#include "polaris/placeholder.hpp"

#include <cstdlib>

int main() {
    if (polaris::add(1, 2) != 3) {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
