package com.hackathon.travel;

import java.util.Objects;

public class City {
	private final String name;
	private final double latitude;
	private final double longitude;

	public City(String name, double latitude, double longitude) {
		this.name = Objects.requireNonNull(name);
		this.latitude = latitude;
		this.longitude = longitude;
	}

	public String getName() { return name; }
	public double getLatitude() { return latitude; }
	public double getLongitude() { return longitude; }

	@Override
	public String toString() {
		return name;
	}

	@Override
	public boolean equals(Object o) {
		if (this == o) return true;
		if (o == null || getClass() != o.getClass()) return false;
		City city = (City) o;
		return name.equalsIgnoreCase(city.name);
	}

	@Override
	public int hashCode() {
		return name.toLowerCase().hashCode();
	}
}
