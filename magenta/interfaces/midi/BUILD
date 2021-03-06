# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Description:
# MIDI interface for Magenta generators.

licenses(["notice"])  # Apache 2.0

py_library(
    name = "midi",
    visibility = [
        # internal notebook binary
    ],
    deps = [
        ":midi_hub",
    ],
)

py_library(
    name = "midi_hub",
    srcs = ["midi_hub.py"],
    deps = [
        "//magenta",
        "@mido//:mido",
    ],
)

py_test(
    name = "midi_hub_test",
    srcs = ["midi_hub_test.py"],
    srcs_version = "PY2AND3",
    deps = [
        ":midi_hub",
        "//magenta",
        "@mido//:mido",
        # tensorflow dep
    ],
)

py_binary(
    name = "magenta_midi",
    srcs = ["magenta_midi.py"],
    visibility = ["//magenta/tools/pip:__subpackages__"],
    deps = [
        ":midi_hub",
        "//magenta",
        "//magenta/models/attention_rnn:attention_rnn_generator",
        "//magenta/models/basic_rnn:basic_rnn_generator",
        "//magenta/models/lookback_rnn:lookback_rnn_generator",
        "@mido//:mido",
    ],
)
