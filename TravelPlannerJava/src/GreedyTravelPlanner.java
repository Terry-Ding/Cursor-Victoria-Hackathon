import java.util.*;

/**
 * Enhanced travel planner that combines greedy nearest-neighbor algorithms
 * with intelligent route planning for start-to-end journeys.
 * Supports both full city tours and intelligent point-to-point travel.
 */
public class GreedyTravelPlanner {
    public static class Result {
        public final List<City> route;
        public final double totalDistanceKm;
        public final List<City> suggestedCities;
        public final String description;
        public final boolean isIntelligentRoute;
        
        // Constructor for traditional greedy results
        Result(List<City> route, double totalDistanceKm) {
            this.route = route;
            this.totalDistanceKm = totalDistanceKm;
            this.suggestedCities = new ArrayList<>();
            this.description = "";
            this.isIntelligentRoute = false;
        }
        
        // Constructor for intelligent route results
        Result(List<City> route, double totalDistanceKm, List<City> suggestedCities, String description) {
            this.route = route;
            this.totalDistanceKm = totalDistanceKm;
            this.suggestedCities = suggestedCities;
            this.description = description;
            this.isIntelligentRoute = true;
        }
    }

    public Result plan(Graph graph, City start, Set<City> mustVisit, boolean returnToStart) {
        List<City> route = new ArrayList<>();
        route.add(start);

        Set<City> remaining = new HashSet<>(mustVisit);
        remaining.remove(start);
        City current = start;
        double distance = 0.0;

        while (!remaining.isEmpty()) {
            City next = null;
            double best = Double.POSITIVE_INFINITY;
            for (City candidate : remaining) {
                double d = shortestEdgeDistance(graph, current, candidate);
                if (d < best) { 
                    best = d; 
                    next = candidate; 
                }
            }
            if (next == null || best == Double.POSITIVE_INFINITY) {
                throw new IllegalStateException("No reachable next city from " + current);
            }
            distance += best;
            route.add(next);
            current = next;
            remaining.remove(next);
        }

        if (returnToStart && route.size() > 1) {
            double back = shortestEdgeDistance(graph, current, start);
            distance += back;
            route.add(start);
        }

        return new Result(route, distance);
    }

    /**
     * Plans an intelligent route from start to end city using Dijkstra's algorithm.
     * Finds the shortest path and suggests interesting cities along the way.
     */
    public Result planIntelligentRoute(Graph graph, City start, City end, List<City> allCities) {
        // Calculate direct distance from start to end
        double directDistance = haversine(
            start.getLatitude(), start.getLongitude(),
            end.getLatitude(), end.getLongitude()
        );
        
        // Use Dijkstra's algorithm to find shortest path
        DijkstraResult dijkstraResult = dijkstra(graph, start, end);
        List<City> shortestRoute = dijkstraResult.path;
        double shortestDistance = dijkstraResult.distance;
        
        // Find cities that are "on the way" or make interesting detours
        List<City> suggestedCities = findInterestingCities(graph, start, end, allCities);
        
        // Build the optimal route using Dijkstra's path as base
        List<City> route = buildOptimalRouteWithDijkstra(graph, start, end, suggestedCities, shortestRoute);
        
        // Calculate total distance
        double totalDistance = calculateRouteDistance(graph, route);
        
        // Generate description
        String description = generateRouteDescription(start, end, suggestedCities, directDistance, totalDistance, shortestDistance);
        
        return new Result(route, totalDistance, suggestedCities, description);
    }
    
    /**
     * Dijkstra's algorithm implementation for finding shortest path between two cities
     */
    private DijkstraResult dijkstra(Graph graph, City start, City end) {
        Map<City, Double> distances = new HashMap<>();
        Map<City, City> previous = new HashMap<>();
        PriorityQueue<City> unvisited = new PriorityQueue<>((a, b) -> 
            Double.compare(distances.getOrDefault(a, Double.POSITIVE_INFINITY), 
                          distances.getOrDefault(b, Double.POSITIVE_INFINITY)));
        
        // Initialize distances
        for (City city : graph.cities()) {
            distances.put(city, Double.POSITIVE_INFINITY);
        }
        distances.put(start, 0.0);
        unvisited.addAll(graph.cities());
        
        while (!unvisited.isEmpty()) {
            City current = unvisited.poll();
            
            if (current.equals(end)) {
                break; // Found destination
            }
            
            double currentDistance = distances.get(current);
            if (currentDistance == Double.POSITIVE_INFINITY) {
                break; // No path exists
            }
            
            // Check all neighbors
            for (Edge edge : graph.neighbors(current)) {
                City neighbor = edge.getTo();
                double newDistance = currentDistance + edge.getDistanceKm();
                
                if (newDistance < distances.get(neighbor)) {
                    distances.put(neighbor, newDistance);
                    previous.put(neighbor, current);
                    unvisited.remove(neighbor); // Remove and re-add to update priority
                    unvisited.add(neighbor);
                }
            }
        }
        
        // Reconstruct path
        List<City> path = new ArrayList<>();
        City current = end;
        while (current != null) {
            path.add(0, current);
            current = previous.get(current);
        }
        
        return new DijkstraResult(path, distances.get(end));
    }
    
    /**
     * Helper class for Dijkstra results
     */
    private static class DijkstraResult {
        final List<City> path;
        final double distance;
        
        DijkstraResult(List<City> path, double distance) {
            this.path = path;
            this.distance = distance;
        }
    }
    
    /**
     * Finds cities that are interesting to visit along the route from start to end.
     * A city is considered interesting if:
     * 1. It's roughly in the direction of travel (not too far off the direct path)
     * 2. It adds reasonable distance to the journey
     * 3. It's not the start or end city
     */
    private List<City> findInterestingCities(Graph graph, City start, City end, List<City> allCities) {
        List<City> interesting = new ArrayList<>();
        double directDistance = haversine(
            start.getLatitude(), start.getLongitude(),
            end.getLatitude(), end.getLongitude()
        );
        
        for (City city : allCities) {
            if (city.equals(start) || city.equals(end)) {
                continue; // Skip start and end cities
            }
            
            // Calculate distances
            double distToStart = haversine(
                start.getLatitude(), start.getLongitude(),
                city.getLatitude(), city.getLongitude()
            );
            double distToEnd = haversine(
                city.getLatitude(), city.getLongitude(),
                end.getLatitude(), end.getLongitude()
            );
            
            // Check if this city is "on the way" - the detour shouldn't be too expensive
            double detourCost = (distToStart + distToEnd) - directDistance;
            double maxAcceptableDetour = directDistance * 0.5; // Allow up to 50% detour
            
            // Also check if the city is reasonably close to the direct path
            double pathDeviation = calculatePathDeviation(start, end, city);
            double maxDeviation = directDistance * 0.3; // Allow up to 30% deviation from direct path
            
            if (detourCost <= maxAcceptableDetour && pathDeviation <= maxDeviation) {
                interesting.add(city);
            }
        }
        
        // Sort by how "on the way" they are (lower detour cost is better)
        interesting.sort((a, b) -> {
            double detourA = calculateDetourCost(start, end, a);
            double detourB = calculateDetourCost(start, end, b);
            return Double.compare(detourA, detourB);
        });
        
        // Limit to top 3 most interesting cities to avoid overwhelming the user
        return interesting.subList(0, Math.min(3, interesting.size()));
    }
    
    /**
     * Calculates how much extra distance would be added by visiting this city
     */
    private double calculateDetourCost(City start, City end, City city) {
        double directDistance = haversine(
            start.getLatitude(), start.getLongitude(),
            end.getLatitude(), end.getLongitude()
        );
        double viaCityDistance = haversine(
            start.getLatitude(), start.getLongitude(),
            city.getLatitude(), city.getLongitude()
        ) + haversine(
            city.getLatitude(), city.getLongitude(),
            end.getLatitude(), end.getLongitude()
        );
        return viaCityDistance - directDistance;
    }
    
    /**
     * Calculates how far a city deviates from the direct path from start to end
     */
    private double calculatePathDeviation(City start, City end, City city) {
        // Use the perpendicular distance from the city to the line from start to end
        // This is a simplified calculation using the cross product
        double startToCity = haversine(
            start.getLatitude(), start.getLongitude(),
            city.getLatitude(), city.getLongitude()
        );
        double startToEnd = haversine(
            start.getLatitude(), start.getLongitude(),
            end.getLatitude(), end.getLongitude()
        );
        
        // Simple approximation: if the city is very close to start or end, deviation is small
        if (startToCity < startToEnd * 0.1 || startToCity > startToEnd * 0.9) {
            return 0;
        }
        
        // For cities in the middle, estimate deviation based on angle
        double cityToEnd = haversine(
            city.getLatitude(), city.getLongitude(),
            end.getLatitude(), end.getLongitude()
        );
        
        // If the sum of distances to start and end is close to direct distance, city is on the path
        double pathSum = startToCity + cityToEnd;
        return Math.abs(pathSum - startToEnd);
    }
    
    /**
     * Builds the optimal route using Dijkstra's shortest path as a base.
     * This method is necessary for advanced route planning and may be used by other planners or future features.
     */
    private List<City> buildOptimalRouteWithDijkstra(Graph graph, City start, City end, List<City> suggestedCities, List<City> shortestRoute) {
        if (suggestedCities.isEmpty()) {
            // Return Dijkstra's shortest path
            return new ArrayList<>(shortestRoute);
        }
        
        // If suggested cities are on the shortest path, use that
        List<City> route = new ArrayList<>();
        route.add(start);
        
        // Check which suggested cities are on or near the shortest path
        List<City> pathCities = new ArrayList<>();
        for (City city : suggestedCities) {
            if (shortestRoute.contains(city)) {
                pathCities.add(city);
            }
        }
        
        if (!pathCities.isEmpty()) {
            // Use Dijkstra's path with suggested cities
            for (City city : shortestRoute) {
                if (!city.equals(start)) {
                    route.add(city);
                    if (city.equals(end)) break;
                }
            }
        } else {
            // Use greedy approach for suggested cities not on shortest path
            List<City> remaining = new ArrayList<>(suggestedCities);
            City current = start;
            
            while (!remaining.isEmpty()) {
                City next = null;
                double bestDistance = Double.POSITIVE_INFINITY;
                
                for (City candidate : remaining) {
                    double distance = haversine(
                        current.getLatitude(), current.getLongitude(),
                        candidate.getLatitude(), candidate.getLongitude()
                    );
                    if (distance < bestDistance) {
                        bestDistance = distance;
                        next = candidate;
                    }
                }
                
                if (next != null) {
                    route.add(next);
                    current = next;
                    remaining.remove(next);
                }
            }
            
            // Add the end city
            route.add(end);
        }
        
        return route;
    }
    
    
    /**
     * Calculates the total distance of a route
     */
    private double calculateRouteDistance(Graph graph, List<City> route) {
        double totalDistance = 0.0;
        for (int i = 0; i < route.size() - 1; i++) {
            City from = route.get(i);
            City to = route.get(i + 1);
            totalDistance += haversine(
                from.getLatitude(), from.getLongitude(),
                to.getLatitude(), to.getLongitude()
            );
        }
        return totalDistance;
    }
    
    /**
     * Generates a human-readable description of the route.
     * This method is necessary for advanced route planning and may be used by other planners or future features.
     */
    @SuppressWarnings("unused")
    private String generateRouteDescription(City start, City end, List<City> suggestedCities, 
                                          double directDistance, double totalDistance, double shortestDistance) {
        StringBuilder desc = new StringBuilder();
        desc.append(String.format("Travel from %s to %s:\n", start.getName(), end.getName()));
        desc.append(String.format("Direct distance: %.1f km\n", directDistance));
        desc.append(String.format("Shortest path (Dijkstra): %.1f km\n", shortestDistance));
        
        if (suggestedCities.isEmpty()) {
            desc.append("No interesting cities found along the route.\n");
            desc.append("Using Dijkstra's shortest path for optimal travel.");
        } else {
            desc.append(String.format("Suggested cities to visit: %s\n", 
                String.join(", ", suggestedCities.stream().map(City::getName).toArray(String[]::new))));
            desc.append(String.format("Total route distance: %.1f km (%.1f km detour from shortest path)\n", 
                totalDistance, totalDistance - shortestDistance));
            desc.append("This route offers interesting stops while keeping the detour reasonable.");
        }
        
        return desc.toString();
    }
    
    // (legacy generateRouteDescription method removed as it was unused)

    private double shortestEdgeDistance(Graph graph, City from, City to) {
        // In this simple model we assume direct edge exists; else approximate by Haversine.
        return graph.neighbors(from).stream()
            .filter(e -> e.getTo().equals(to))
            .mapToDouble(Edge::getDistanceKm)
            .min()
            .orElse(haversine(from.getLatitude(), from.getLongitude(), to.getLatitude(), to.getLongitude()));
    }

    // Haversine distance in KM
    public static double haversine(double lat1, double lon1, double lat2, double lon2) {
        final double R = 6371.0; // km
        double dLat = Math.toRadians(lat2 - lat1);
        double dLon = Math.toRadians(lon2 - lon1);
        double a = Math.sin(dLat/2) * Math.sin(dLat/2)
                + Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2))
                * Math.sin(dLon/2) * Math.sin(dLon/2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return R * c;
    }
}
