# Travel Planner - Java Graph Algorithm 🗺️

A Java-based travel route planner using graph algorithms and greedy optimization for the Victoria Hackathon!

## Overview

This project implements a **greedy nearest-neighbor algorithm** to find efficient travel routes between cities. It uses a complete graph where each city is connected to every other city, with distances calculated using the Haversine formula for real-world geographic distances.

## Features

- 🏙️ **Graph-based city network** - Complete graph with real geographic coordinates
- 🎯 **Greedy algorithm** - Fast nearest-neighbor pathfinding
- 📍 **Real distances** - Haversine formula for accurate Earth distances
- 🚀 **Flexible routing** - Start from any city, optionally return to start
- 📊 **CSV data input** - Easy to add new cities and routes
- ⚡ **Fast execution** - O(n²) complexity for quick results

## Algorithm Details

### Greedy Nearest-Neighbor Approach
1. Start at the specified city (or first city in dataset)
2. At each step, visit the nearest unvisited city
3. Continue until all cities are visited
4. Optionally return to the starting city

**Note**: This is a greedy heuristic, not optimal like TSP algorithms, but provides good results quickly for hackathon demos.

## Project Structure

```
TravelPlannerJava/
├── pom.xml                           # Maven configuration
├── data/
│   └── cities.csv                    # Sample city data (name,lat,lon)
├── src/main/java/com/hackathon/travel/
│   ├── City.java                     # City model with coordinates
│   ├── Edge.java                     # Graph edge with distance
│   ├── Graph.java                    # Graph data structure
│   ├── GreedyTravelPlanner.java      # Main algorithm implementation
│   └── Main.java                     # CLI application entry point
└── README.md                         # This file
```

## Installation & Setup

### Prerequisites
- **Java 17+** (JDK or JRE)
- **Maven 3.6+** (optional, for building)

### Quick Start (Without Maven)

1. **Navigate to project directory**:
   ```bash
   cd TravelPlannerJava
   ```

2. **Compile the project**:
   ```bash
   javac -d out $(find src/main/java -name "*.java")
   ```

3. **Run the travel planner**:
   ```bash
   # Basic usage - visit all cities starting from first city
   java -cp out com.hackathon.travel.Main data/cities.csv
   
   # Start from specific city
   java -cp out com.hackathon.travel.Main data/cities.csv --start Victoria
   
   # Return to starting city (complete round trip)
   java -cp out com.hackathon.travel.Main data/cities.csv --start Victoria --return
   ```

### With Maven (Recommended)

1. **Build the project**:
   ```bash
   cd TravelPlannerJava
   mvn clean package
   ```

2. **Run the executable JAR**:
   ```bash
   # Basic usage
   java -jar target/travel-planner-1.0.0-jar-with-dependencies.jar data/cities.csv
   
   # Start from specific city and return
   java -jar target/travel-planner-1.0.0-jar-with-dependencies.jar data/cities.csv --start Victoria --return
   ```

## Usage Examples

### Example 1: Visit all cities starting from Victoria
```bash
java -cp out com.hackathon.travel.Main data/cities.csv --start Victoria
```
**Output**:
```
Greedy route:
Victoria -> Seattle -> Portland -> San Francisco -> Los Angeles -> Las Vegas -> Phoenix -> Salt Lake City -> Denver -> Vancouver
Total distance: 4523.45 km
```

### Example 2: Round trip from Vancouver
```bash
java -cp out com.hackathon.travel.Main data/cities.csv --start Vancouver --return
```
**Output**:
```
Greedy route:
Vancouver -> Victoria -> Seattle -> Portland -> San Francisco -> Los Angeles -> Las Vegas -> Phoenix -> Salt Lake City -> Denver -> Vancouver
Total distance: 5234.78 km
```

## Data Format

The `data/cities.csv` file contains city information in CSV format:

```csv
# name,lat,lon
Victoria,48.4284,-123.3656
Vancouver,49.2827,-123.1207
Seattle,47.6062,-122.3321
Portland,45.5152,-122.6784
San Francisco,37.7749,-122.4194
Los Angeles,34.0522,-118.2437
Las Vegas,36.1699,-115.1398
Phoenix,33.4484,-112.0740
Salt Lake City,40.7608,-111.8910
Denver,39.7392,-104.9903
```

### Adding New Cities
Simply add new lines to the CSV file:
```csv
New York,40.7128,-74.0060
Boston,42.3601,-71.0589
```

## Technical Implementation

### Graph Model
- **Complete Graph**: Every city connected to every other city
- **Weighted Edges**: Distances calculated using Haversine formula
- **Undirected**: Travel distance is same in both directions

### Distance Calculation
Uses the **Haversine formula** for accurate Earth surface distances:
```java
public static double haversine(double lat1, double lon1, double lat2, double lon2) {
    final double R = 6371.0; // Earth radius in km
    // ... implementation details
}
```

### Algorithm Complexity
- **Time Complexity**: O(n²) where n is number of cities
- **Space Complexity**: O(n²) for the complete graph
- **Practical Performance**: Handles 100+ cities efficiently

## Hackathon Features

This project demonstrates:
- ✅ **Graph algorithms** - Complete graph implementation
- ✅ **Greedy optimization** - Nearest-neighbor heuristic
- ✅ **Real-world data** - Geographic coordinates and distances
- ✅ **Clean Java code** - Object-oriented design
- ✅ **CLI interface** - Easy to demo and use
- ✅ **Maven build** - Professional project structure
- ✅ **Extensible design** - Easy to add new algorithms

## Future Enhancements

- 🚀 **Multiple algorithms** - TSP, genetic algorithms, simulated annealing
- 🗺️ **Visualization** - Map display of routes
- 📊 **Performance metrics** - Algorithm comparison
- 🌐 **Real-time data** - Live traffic and weather integration
- 📱 **Web interface** - Browser-based planning tool

## Development

### Running Tests
```bash
# With Maven
mvn test

# Without Maven (if you add test files)
javac -cp "out:junit-platform-console-standalone.jar" -d out-test src/test/java/**/*.java
java -jar junit-platform-console-standalone.jar --class-path out --scan-classpath
```

### Building for Distribution
```bash
mvn clean package
# Creates: target/travel-planner-1.0.0-jar-with-dependencies.jar
```

---

**Perfect for Hackathon Demo!** 🏆

This project showcases:
- Advanced algorithms and data structures
- Real-world problem solving
- Clean, professional Java code
- Practical application with geographic data
- Easy to extend and modify

**Ready to present!** 🚀