#include "polaris/event_scheduler.hpp"

#include <cassert>

int main() {
    polaris::EventScheduler sched;
    sched.schedule(2.0, 1);
    sched.schedule(1.0, 2);
    sched.schedule(1.0, 1);

    auto first = sched.pop_next();
    assert(first.has_value());
    assert(first->time == 1.0);
    assert(first->id == 1);

    auto second = sched.pop_next();
    assert(second.has_value());
    assert(second->time == 1.0);
    assert(second->id == 2);

    auto third = sched.pop_next();
    assert(third.has_value());
    assert(third->time == 2.0);

    assert(!sched.pop_next().has_value());
    return 0;
}
