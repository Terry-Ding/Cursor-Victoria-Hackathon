#!/bin/bash
# Simple compilation script for the Travel Planner

echo "Compiling Travel Planner..."
javac -d . src/*.java

if [ $? -eq 0 ]; then
    echo "✅ Compilation successful!"
    echo "Run with: java Main data/cities.csv --start Victoria --return"
else
    echo "❌ Compilation failed!"
    exit 1
fi
