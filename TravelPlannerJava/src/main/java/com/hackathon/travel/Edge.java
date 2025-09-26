package com.hackathon.travel;

public class Edge {
	private final City from;
	private final City to;
	private final double distanceKm;

	public Edge(City from, City to, double distanceKm) {
		this.from = from;
		this.to = to;
		this.distanceKm = distanceKm;
	}

	public City getFrom() { return from; }
	public City getTo() { return to; }
	public double getDistanceKm() { return distanceKm; }
}
