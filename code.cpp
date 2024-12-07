#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <tuple>
#include <cmath>
#include <omp.h>

using namespace std;

// Structures
struct Package {
    string identifier;
    int length, width, height, weight;
    char type;  // 'P' for Priority, 'E' for Economy
    int costOfDelay;
    bool packed = false;
    tuple<int, int, int> placement; // Placement coordinates

    int getVolume() const { return length * width * height; }
    double getDensity() const { return static_cast<double>(weight) / getVolume(); }
};

struct ULD {
    string identifier;
    int length, width, height, weightLimit;
    int currentWeight = 0;
    int currentVolume = 0;
    vector<tuple<int, int, int, Package>> packedPackages; // (x, y, z, Package)

    int getRemainingWeight() const { return weightLimit - currentWeight; }
    int getRemainingVolume() const { return length * width * height - currentVolume; }
};

// CSV line splitting function
vector<string> getNextLineAndSplitIntoTokens(istream& str) {
    vector<string> result;
    string line;
    getline(str, line);
    stringstream lineStream(line);
    string cell;

    while (getline(lineStream, cell, ',')) {
        result.push_back(cell);
    }

    if (!lineStream && cell.empty()) {
        result.push_back("");
    }

    return result;
}

// Loaders
vector<ULD> loadULDs(const string& filename) {
    vector<ULD> ulds;
    ifstream file(filename);
    if (!file) {
        cerr << "Error: Unable to open ULD file " << filename << endl;
        exit(1);
    }

    string header;
    getline(file, header); // Skip header line

    while (!file.eof()) {
        vector<string> tokens = getNextLineAndSplitIntoTokens(file);
        if (tokens.size() < 5) continue;

        string id = tokens[0];
        int length = stoi(tokens[1]);
        int width = stoi(tokens[2]);
        int height = stoi(tokens[3]);
        int weightLimit = stoi(tokens[4]);

        ulds.push_back({id, length, width, height, weightLimit});
    }

    return ulds;
}

vector<Package> loadPackages(const string& filename) {
    vector<Package> packages;
    ifstream file(filename);
    if (!file) {
        cerr << "Error: Unable to open Package file " << filename << endl;
        exit(1);
    }

    string header;
    getline(file, header); // Skip header line

    while (!file.eof()) {
        vector<string> tokens = getNextLineAndSplitIntoTokens(file);
        if (tokens.size() < 6) continue;

        string id = tokens[0];
        int length = stoi(tokens[1]);
        int width = stoi(tokens[2]);
        int height = stoi(tokens[3]);
        int weight = stoi(tokens[4]);
        char type = tokens[5] == "Priority" ? 'P' : 'E';
        int costOfDelay = (tokens.size() > 6 && type == 'E') ? stoi(tokens[6]) : 0;

        packages.push_back({id, length, width, height, weight, type, costOfDelay});
    }

    return packages;
}

// Improved Space Fallback Placement
bool improvedSpacePlacement(ULD& uld, Package& pkg) {
    for (int x = 0; x + pkg.length <= uld.length; x++) {
        for (int y = 0; y + pkg.width <= uld.width; y++) {
            for (int z = 0; z + pkg.height <= uld.height; z++) {
                if (uld.currentWeight + pkg.weight <= uld.weightLimit &&
                    uld.currentVolume + (pkg.length * pkg.width * pkg.height) <= uld.length * uld.width * uld.height) {
                    uld.packedPackages.emplace_back(x, y, z, pkg);
                    uld.currentWeight += pkg.weight;
                    uld.currentVolume += pkg.length * pkg.width * pkg.height;
                    pkg.placement = {x, y, z};
                    return true;
                }
            }
        }
    }
    return false;
}

// Refactored intelligent package placement
bool intelligentPackagePlacement(ULD& uld, Package& pkg) {
    struct Box {
        int x, y, z, length, width, height;
    };

    auto doesOverlap = [](const Box& b1, const Box& b2) {
        return !(b1.x + b1.length <= b2.x ||
                 b2.x + b2.length <= b1.x ||
                 b1.y + b1.width <= b2.y ||
                 b2.y + b2.width <= b1.y ||
                 b1.z + b1.height <= b2.z ||
                 b2.z + b2.height <= b1.z);
    };

    vector<tuple<int, int, int>> rotations = {
        {pkg.length, pkg.width, pkg.height},
        {pkg.width, pkg.height, pkg.length},
        {pkg.height, pkg.length, pkg.width},
        {pkg.length, pkg.height, pkg.width},
        {pkg.width, pkg.length, pkg.height},
        {pkg.height, pkg.width, pkg.length}
    };

    for (const auto& rotation : rotations) {
        int l = get<0>(rotation);
        int w = get<1>(rotation);
        int h = get<2>(rotation);

        if (l > uld.length || w > uld.width || h > uld.height) continue;

        if (uld.currentWeight + pkg.weight <= uld.weightLimit &&
            uld.currentVolume + (l * w * h) <= uld.length * uld.width * uld.height) {
            uld.packedPackages.emplace_back(0, 0, 0, pkg);
            uld.currentWeight += pkg.weight;
            uld.currentVolume += l * w * h;
            pkg.placement = {0, 0, 0};
            return true;
        }
    }

    return false;
}

// Main optimization logic
class AdvancedPackingOptimizer {
private:
    vector<Package> packages;
    vector<ULD> ulds;
    int priorityCost;

public:
    AdvancedPackingOptimizer(const vector<Package>& pkgs, const vector<ULD>& containers, int priorityCost)
        : packages(pkgs), ulds(containers), priorityCost(priorityCost) {}

    vector<ULD> optimize() {
        #pragma omp parallel for
        for (size_t i = 0; i < packages.size(); ++i) {
            Package& pkg = packages[i];
            if (pkg.packed) continue;

            for (auto& uld : ulds) {
                if (intelligentPackagePlacement(uld, pkg) ||
                    improvedSpacePlacement(uld, pkg)) {
                    #pragma omp critical
                    {
                        pkg.packed = true;
                    }
                    break;
                }
            }
        }

        return ulds;
    }
    void generateOutput(const string& filename) {
        ofstream outputFile(filename);
        if (!outputFile) {
            cerr << "Error opening output file!" << endl;
            return;
        }

        unordered_set<string> packedPackageIds;
        for (const auto& uld : ulds) {
            for (const auto& entry : uld.packedPackages) {
                int x = get<0>(entry);
                int y = get<1>(entry);
                int z = get<2>(entry);
                const Package& pkg = get<3>(entry);
                outputFile << pkg.identifier << "," << uld.identifier
                           << "," << x << "," << y << "," << z
                           << "," << pkg.length << "," << pkg.width << "," << pkg.height << "\n";
                packedPackageIds.insert(pkg.identifier);
            }
        }

        for (const auto& pkg : packages) {
            if (packedPackageIds.find(pkg.identifier) == packedPackageIds.end()) {
                outputFile << pkg.identifier << ",NONE,-1,-1,-1,-1,-1,-1\n";
            }
        }
    }
};

int main() {
    string uldFile = "C:\\Users\\rashm\\OneDrive\\Documents\\Fedex\\fedex\\uld.csv";
    string packageFile = "C:\\Users\\rashm\\OneDrive\\Documents\\Fedex\\fedex\\packages.csv";

    vector<ULD> ulds = loadULDs(uldFile);
    vector<Package> packages = loadPackages(packageFile);
    

    AdvancedPackingOptimizer optimizer(packages, ulds, 40);
    optimizer.optimize();
    optimizer.generateOutput("output.csv");

    return 0;
}
