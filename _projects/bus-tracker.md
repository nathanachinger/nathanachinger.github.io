---
title: "Bus Tracker"
excerpt: "Custom IOT device for live display of bus stop arrival times."
collection: projects
antenna_gallery:
  - url: bus_tracker_antenna_schematic.png
    image_path: bus_tracker_antenna_schematic.png
    alt: "Wifi trace antenna schematic"
  - url: bus_tracker_antenna_realistic.png
    image_path: bus_tracker_antenna_realistic.png
    alt: "Wifi trace antenna 3D view"
  - url: bus_tracker_antenna_copper.png
    image_path: bus_tracker_antenna_copper.png
    alt: "Wifi trace antenna copper layout"
backlight_gallery:
  - url: bus_tracker_light_sensor_schematic.png
    image_path: bus_tracker_light_sensor_schematic.png
    alt: "Light sensor schematic"
  - url: bus_tracker_light_sensor_realistic.png
    image_path: bus_tracker_light_sensor_realistic.png
    alt: "Light sensor 3D view"
  - url: bus_tracker_light_sensor_copper.png
    image_path: bus_tracker_light_sensor_copper.png
    alt: "Light sensor copper layout"
micro_gallery:
  - url: bus_tracker_micro_schematic.png
    image_path: bus_tracker_micro_schematic.png
    alt: "ESP32-C3 microcontroller schematic"
  - url: bus_tracker_micro_realistic.png
    image_path: bus_tracker_micro_realistic.png
    alt: "ESP32-C3 microcontroller 3D view"
  - url: bus_tracker_micro_copper.png
    image_path: bus_tracker_micro_copper.png
    alt: "ESP32-C3 microcontroller copper layout"
power_gallery:
  - url: bus_tracker_usb_power_schematic.png
    image_path: bus_tracker_usb_power_schematic.png
    alt: "USB power schematic"
  - url: bus_tracker_usb_power_realistic.png
    image_path: bus_tracker_usb_power_realistic.png
    alt: "USB power 3D view"
  - url: bus_tracker_usb_power_copper.png
    image_path: bus_tracker_usb_power_copper.png
    alt: "USB power copper layout"
---

## Overview

I created this project because I was tired of checking the bus times on my phone every morning for my stop. This device is intended to be connected to your home Wifi network and sit in the kitchen, displaying the live arrival times for your bus stop.

## Hardware

[Schematic]({{ site.baseurl }}/images/bus_tracker_schematic.pdf){:target="_blank" rel="noopener"} · [PCB]({{ site.baseurl }}/images/bus_tracker_pcb.pdf){:target="_blank" rel="noopener"}

### Wifi Trace Antenna

Features a 2.4Ghz trace antenna for Wifi connection. Followed high-frequency layout principles including trace width calculation and a PI impedance matching network for best the Wifi range performance.

{% include gallery id="antenna_gallery" %}

### Auto-Dimming Backlight

A phototransistor senses the ambient light in the room to dynamically adjust the backlight brightness of the display. A resistor biases the phototransistor to create a voltage divider, which output is measured by an internal ADC on the microcontroller. The display backlight is driven by a PWM signal. The duty cycle is adjusted based on the ambient light in the room.

{% include gallery id="backlight_gallery" %}

### Color LCD Display
A color LCD display is connected over SPI

### Microcontroller

Uses an ESP32-C3 microcontroller for its modern architecture, low power consumption, wireless connectivity, integrated USB to JTAG programmer, and low cost. Paired with a 4Mb external SPI flash for program storage.

{% include gallery id="micro_gallery" %}

### Power and USB
An LDO converts the 5V USB input to 3.3V for the microcontroller. A linear regulator was chosen for its simplicity and because of the small drop required between the input and output voltages.

{% include gallery id="power_gallery" %}

## Firmware