#include "polaris/event_scheduler.hpp"

namespace polaris {

void EventScheduler::schedule(double time, int id) { queue_.push(ScheduledEvent{time, id}); }

std::optional<ScheduledEvent> EventScheduler::pop_next() {
    if (queue_.empty()) {
        return std::nullopt;
    }
    ScheduledEvent next = queue_.top();
    queue_.pop();
    return next;
}

std::size_t EventScheduler::size() const { return queue_.size(); }

} // namespace polaris
