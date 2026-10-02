# Antenna notes — Pi 5 gateway

**Evidence:** DESIGNED

Gateway reference uses a **868 MHz** concentrator antenna (see `configs/devices/gateway-pi5.yaml` `rx_channels`). Same FSPL simulation path as field nodes.

## Store-and-forward vs RF

Antenna quality affects `packets_rx` in the Digital Testbed only through abstract `packet_loss` and RSSI stubs — not EM simulation.

## Non-claims

No deployed gateway performance data. No carrier LTE antenna integration beyond YAML `backhaul.fallback: lte` (**DESIGNED**).
