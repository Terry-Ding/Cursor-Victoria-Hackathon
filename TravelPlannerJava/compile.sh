#!/bin/bash
# Simple compilation script for the Travel Planner

echo "Compiling Travel Planner..."
javac -d out src/*.java

if [ $? -eq 0 ]; then
    echo "✅ Compilation successful!"
    echo "Run with: java -cp out Main data/cities.csv --start [City-1] --end [City-2]"
    echo "Or: java -cp out Main data/cities.csv --start Nanaimo --return (round trip)"
else
    echo "❌ Compilation failed!"
    exit 1
fi
