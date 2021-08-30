// Authors: Rafael Z. Palierini and Rubens de A. R. Mendes.
// Data: August 28th, 2021.

// Libraries
#include <iostream>
#include <fstream>
#include <string>
#include <thread>
#include <chrono>

// ============================================================
//							IMPORTANTE
// ============================================================
// 
// MUDE AS VARIÁVEIS ABAIXO PARA UTILIZAR O CÓDIGO COMO DESEJA!
//
// Global variables
//
// These determines how the program runs.
const int TOTAL_THREADS = 12; // The total of Threads are gonna be used.
const int MIN_THREADS = 12; // Minimun of the Threads are gonna be used (This one must be lesser or equal the TOTAL_THREADS).
const int TOTAL_RUNS = 150; // How many runs you'll do to take the average time per group of threads.
const bool SINGLE = false; // Set it true to run a single-thread example.












// This function is responsible for calculating the prime numbers. Your complexity is O(sqrt(n)).
// Parameter:
//		int n = Number to be tested.
// 
// Extracted from: https://www.geeksforgeeks.org/prime-numbers/
bool isPrime(int n) {

	if (n == 0 || n == 1) {
		return false;
	}

	for (int i = 2; i <= sqrt(n); i++)
		if (n % i == 0)
			return false;

	return true;
}

// This function is responsible for taking all numbers from data.csv and then put them in an array of int.
// Parameter:
//		int* n = The array to be saved with all numbers.
//
// Extracted from: Original.
void getNumbers(int* n) {
	std::string tempString;
	std::ifstream file("data.csv");

	int i = 0;

	while (getline(file, tempString)) {

		n[i] = std::stoi(tempString);
		i++;
	}

	file.close();

	return;
}

// This function is responsible for taking all primes and non primes with a single-thread.
// Parameter:
//		int* n = The array with all numbers.
//		int* totalPrime = Where the total of primes should be stored.
//		int* totalNoPrime = Where the total of non primes should be stored.
//
// Extracted from: Original.
void sThreadPrime(int* n, int* totalPrime, int* totalNoPrime) {
	int i = 0;
	int noPrime = 0;
	int prime = 0;
	while (i < 250000) {

		if (isPrime(n[i])) {
			prime++;
		}

		else {
			noPrime++;
		}

		i++;
	}

	*totalPrime = prime;
	*totalNoPrime = noPrime;

	return;
}

// This function is responsible for taking all primes and non primes with a single-thread.
// Parameter:
//		int* n = The array with all numbers.
//		int qThreads = The quantity of Threads are going to be used.
//		int init = The initial index of that Thread.
//		int* vPrime = Where the total of primes should be stored by Thread.
//		int* nPrime = Where the total of non primes should be stored by Thread.
//
// Extracted from: Original.
void mThreadPrime(int* n, int qThreads, int init, int* vPrime, int* nPrime) {
	
	int i = init;
	int noPrime = 0;
	int prime = 0;
	while (i < 250000) {

		if (isPrime(n[i])) {
			prime++;
		}

		else {
			noPrime++;
		}

		i += qThreads;
	}

	vPrime[init] = prime;
	nPrime[init] = noPrime;

	return;
}

// Just a rather simple main function.
//
// Extracted from: Original.
int main()
{
	int n[250000]; // Array to store all numbers.

	clock_t start, end;  // Variables to store the start time and the end time.

	getNumbers(n);

	int vPrime[12]; // Array to store the total of primes by Thread.
	int nPrime[12]; // Array to store the total of non-primes by Thread.

	int totalPrimes = 0; // Variable to store the total of primes by a Single-Thread.
	int totalNoPrimes = 0; // Variable to store the total of non primes by a Single-Thread.

	float singleTime; // Store the Single-Thread time.

	
	if (SINGLE) {
		start = clock(); // Start the counter.
		sThreadPrime(n, &totalPrimes, &totalNoPrimes);
		end = clock(); // End the counter.

		singleTime = ((float)end - start) / CLOCKS_PER_SEC;


		// Print the results.
		std::cout << "SINGLE-THREAD" << std::endl;
		std::cout << "===========================================================" << std::endl;
		std::cout << "PRIMES: " << totalPrimes << " | " << "NON-PRIMES: " << totalNoPrimes << std::endl;
		std::cout << "TOTAL: " << totalNoPrimes + totalPrimes << std::endl;
		std::cout << "TOTAL TIME: " << singleTime << "s" << std::endl;
		std::cout << std::endl;
	}

	float runs[TOTAL_RUNS]; // Store how many runs the program should do.
	int cRun; // Store how many runs the program did.
	int tempTotal = MIN_THREADS; // Store the total of Threads done.
	float average[TOTAL_THREADS] = {}; // Store the average by Thread.

	// Do the Multi-Thread process.
	std::cout << " STARTING MULTI-THREAD:" << std::endl;
	while (tempTotal < TOTAL_THREADS + 1) {
		cRun = 0;

		std::cout << tempTotal << " THREADS PROCESSING..." << std::endl;

		while (cRun < TOTAL_RUNS) {
			start = clock(); // Start the counting of this run

			std::thread mThread[TOTAL_THREADS];

			for (int i = 0; i < tempTotal; i++) {
				mThread[i] = std::thread(mThreadPrime, n, tempTotal, i, vPrime, nPrime);
			}

			for (int i = 0; i < tempTotal; i++) {
				mThread[i].join();
			}

			end = clock(); // End the counting of this run

			runs[cRun] = ((float)end - start) / CLOCKS_PER_SEC;

			cRun++;
		}

		// Take the average time of all the runs.
		for (int i = 0; i < TOTAL_RUNS; i++) {
			average[tempTotal - 1] += runs[i];
		}
		average[tempTotal - 1] /= TOTAL_RUNS;

		std::cout << tempTotal << " THREADS DONE!" << std::endl;

		tempTotal++;
	}

	totalPrimes = 0;
	totalNoPrimes = 0;

	for (int i = 0; i < TOTAL_THREADS; i++) {
		totalPrimes += vPrime[i];
		totalNoPrimes += nPrime[i];
	}

	// Show the results of Multi-Thread.
	std::cout << std::endl;
	std::cout << "MULTI-THREAD" << std::endl;
	std::cout << "===========================================================" << std::endl;
	std::cout << "PRIMES: " << totalPrimes << " | " << "NON-PRIMES: " << totalNoPrimes << std::endl;
	std::cout << "TOTAL: " << totalNoPrimes + totalPrimes << std::endl;
	std::cout << std::endl;

	// Print the average time for all quantity of Threads tested.
	for (int i = MIN_THREADS; i < TOTAL_THREADS + 1; i++) {
		std::cout << "THREADS " << i << " TOTAL TIME: " << average[i-1] << "s" << std::endl;
	}

	std::cout << std::endl;

	// Print the speed up for all quantity of Threads tested.
	if (SINGLE) {
		for (int i = MIN_THREADS; i < TOTAL_THREADS + 1; i++) {
			std::cout << "THREADS " << i << " SPEED UP: " << (singleTime/average[i - 1]) << "x" << std::endl;
		}
	}

	return 0;
}
