package com.hackathon.travel;

import java.util.*;

public class Graph {
	private final Map<City, List<Edge>> adjacency = new HashMap<>();

	public void addCity(City city) {
		adjacency.computeIfAbsent(city, c -> new ArrayList<>());
	}

	public void addUndirectedEdge(City a, City b, double distanceKm) {
		addCity(a);
		addCity(b);
		adjacency.get(a).add(new Edge(a, b, distanceKm));
		adjacency.get(b).add(new Edge(b, a, distanceKm));
	}

	public List<Edge> neighbors(City city) {
		return adjacency.getOrDefault(city, Collections.emptyList());
	}

	public Set<City> cities() { return adjacency.keySet(); }
}
