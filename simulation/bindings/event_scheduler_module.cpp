#include "polaris/event_scheduler.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(polaris_event_scheduler, m) {
    m.doc() = "Minimal deterministic event scheduler (P6 optional binding)";

    py::class_<polaris::ScheduledEvent>(m, "ScheduledEvent")
        .def_readonly("time", &polaris::ScheduledEvent::time)
        .def_readonly("id", &polaris::ScheduledEvent::id);

    py::class_<polaris::EventScheduler>(m, "EventScheduler")
        .def(py::init<>())
        .def("schedule", &polaris::EventScheduler::schedule)
        .def("pop_next", &polaris::EventScheduler::pop_next)
        .def("size", &polaris::EventScheduler::size);
}
