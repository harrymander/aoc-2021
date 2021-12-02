#include <iostream>
#include <fstream>
#include <string>

static void part_a(const char *filename)
{
	int horiz = 0;
	int depth = 0;

	std::ifstream file(filename);
	std::string command;
	int steps;
	while (file >> command >> steps) {
		if (command == "forward")
			horiz += steps;
		else if (command == "down")
			depth += steps;
		else
			depth -= steps;
	}

	std::cout << horiz * depth << std::endl;
}

static void part_b(const char *filename)
{
	int horiz = 0;
	int depth = 0;
	int aim = 0;

	std::ifstream file(filename);
	std::string command;
	int steps;
	while (file >> command >> steps) {
		if (command == "forward") {
			horiz += steps;
			depth += steps * aim;
		} else if (command == "down") {
			aim += steps;
		} else {
			aim -= steps;
		}
	}

	std::cout << horiz * depth << std::endl;
}


int main(int argc, char const *argv[])
{
	const char *filename = argv[1];
	if (!filename)
		return 1;

	part_a(filename);
	part_b(filename);

	return 0;
}
