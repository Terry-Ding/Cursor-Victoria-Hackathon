package com.hackathon.travel;

import java.util.*;

/**
 * Greedy nearest-neighbor path starting from a source city visiting all targets.
 * Not optimal like TSP, but fast and simple for demos.
 */
public class GreedyTravelPlanner {
	public static class Result {
		public final List<City> route;
		public final double totalDistanceKm;
		Result(List<City> route, double totalDistanceKm) {
			this.route = route;
			this.totalDistanceKm = totalDistanceKm;
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
				if (d < best) { best = d; next = candidate; }
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
