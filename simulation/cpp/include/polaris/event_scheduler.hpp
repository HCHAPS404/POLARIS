#pragma once

#include <cstdint>
#include <optional>
#include <queue>
#include <vector>

namespace polaris {

struct ScheduledEvent {
    double time;
    int id;
};

inline bool operator<(const ScheduledEvent &a, const ScheduledEvent &b) {
    if (a.time != b.time) {
        return a.time > b.time;
    }
    return a.id > b.id;
}

class EventScheduler {
  public:
    void schedule(double time, int id);
    std::optional<ScheduledEvent> pop_next();
    std::size_t size() const;

  private:
    std::priority_queue<ScheduledEvent> queue_;
};

} // namespace polaris
