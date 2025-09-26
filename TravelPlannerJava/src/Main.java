import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        if (args.length == 0) {
            System.out.println("Usage: java Main <cities.csv> [--start CityName] [--end CityName] [--return]");
            System.out.println("Example: java Main data/cities.csv --start Victoria --end Tofino");
            System.out.println("Example: java Main data/cities.csv --start Nanaimo --end Campbell River --return");
            return;
        }

        String csvPath = args[0];
        String startName = null;
        String endName = null;
        boolean returnToStart = false;

        for (int i = 1; i < args.length; i++) {
            if ("--start".equals(args[i]) && i + 1 < args.length) {
                startName = args[++i];
            } else if ("--end".equals(args[i]) && i + 1 < args.length) {
                endName = args[++i];
            } else if ("--return".equals(args[i])) {
                returnToStart = true;
            }
        }

        List<City> cities = loadCities(csvPath);
        Graph graph = buildCompleteGraph(cities);
        City start = startName != null ? findCity(cities, startName) : cities.get(0);
        City end = endName != null ? findCity(cities, endName) : null;

        GreedyTravelPlanner planner = new GreedyTravelPlanner();

        if (end != null) {
            // Use intelligent route planning for start-to-end route
            GreedyTravelPlanner.Result result = planner.planIntelligentRoute(graph, start, end, cities);

            System.out.println("=== DIJKSTRA TRAVEL PLANNER ===");
            System.out.println(result.description);
            System.out.println();
            System.out.println("Recommended route:");
            for (int i = 0; i < result.route.size(); i++) {
                City c = result.route.get(i);
                System.out.print(c.getName());
                if (i < result.route.size() - 1)
                    System.out.print(" -> ");
            }
            System.out.println();
            System.out.printf("Direct distance: %.2f km\n", result.totalDistanceKm);

            if (!result.suggestedCities.isEmpty()) {
                System.out.println();
                System.out.println("Cities you can visit along the way:");
                for (City city : result.suggestedCities) {
                    double detourCost = calculateDetourCost(start, end, city);
                    System.out.printf("- %s (adds %.1f km to your journey)\n", city.getName(), detourCost);
                }
            }
        } else {
            // Use traditional greedy planner for round-trip
            GreedyTravelPlanner.Result result = planner.plan(graph, start, new HashSet<>(cities), returnToStart);

            System.out.println("Greedy route (visiting all cities):");
            for (int i = 0; i < result.route.size(); i++) {
                City c = result.route.get(i);
                System.out.print(c.getName());
                if (i < result.route.size() - 1)
                    System.out.print(" -> ");
            }
            System.out.println();
            System.out.printf("Direct distance: %.2f km\n", result.totalDistanceKm);
        }
    }

    private static List<City> loadCities(String csvPath) throws Exception {
        List<City> list = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(csvPath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#"))
                    continue;
                // name,lat,lon
                String[] parts = line.split(",");
                if (parts.length < 3)
                    continue;
                list.add(new City(parts[0].trim(), Double.parseDouble(parts[1]), Double.parseDouble(parts[2])));
            }
        }
        return list;
    }

    private static Graph buildCompleteGraph(List<City> cities) {
        Graph g = new Graph();
        for (City a : cities) {
            g.addCity(a);
        }
        for (int i = 0; i < cities.size(); i++) {
            for (int j = i + 1; j < cities.size(); j++) {
                City a = cities.get(i), b = cities.get(j);
                double d = GreedyTravelPlanner.haversine(a.getLatitude(), a.getLongitude(), b.getLatitude(),
                        b.getLongitude());
                g.addUndirectedEdge(a, b, d);
            }
        }
        return g;
    }

    private static City findCity(List<City> cities, String name) {
        return cities.stream().filter(c -> c.getName().equalsIgnoreCase(name)).findFirst()
                .orElseThrow(() -> new IllegalArgumentException("City not found: " + name));
    }

    private static double calculateDetourCost(City start, City end, City city) {
        double directDistance = GreedyTravelPlanner.haversine(
                start.getLatitude(), start.getLongitude(),
                end.getLatitude(), end.getLongitude());
        double viaCityDistance = GreedyTravelPlanner.haversine(
                start.getLatitude(), start.getLongitude(),
                city.getLatitude(), city.getLongitude())
                + GreedyTravelPlanner.haversine(
                        city.getLatitude(), city.getLongitude(),
                        end.getLatitude(), end.getLongitude());
        return viaCityDistance - directDistance;
    }
}
