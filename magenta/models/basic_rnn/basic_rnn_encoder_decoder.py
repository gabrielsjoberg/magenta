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
"""A MelodyEncoderDecoder specific to the basic RNN model."""

# internal imports
import magenta

NUM_SPECIAL_MELODY_EVENTS = magenta.music.NUM_SPECIAL_MELODY_EVENTS

MIN_NOTE = 48  # Inclusive
MAX_NOTE = 84  # Exclusive
TRANSPOSE_TO_KEY = 0  # C Major


class MelodyEncoderDecoder(magenta.music.MelodyEncoderDecoder):
  """A MelodyEncoderDecoder specific to the lookback RNN model.

  Attributes:
    _num_model_events: The number of different melody events that can be
        generated by this model.
  """

  def __init__(self):
    """Initializes the MelodyEncoderDecoder."""
    super(MelodyEncoderDecoder, self).__init__(MIN_NOTE, MAX_NOTE,
                                               TRANSPOSE_TO_KEY)
    self._num_model_events = (self.max_note - self.min_note +
                              NUM_SPECIAL_MELODY_EVENTS)

  @property
  def input_size(self):
    return self._num_model_events

  @property
  def num_classes(self):
    return self._num_model_events

  def melody_event_to_model_event(self, melody_event):
    """Collapses a melody event value into a zero-based index range.

    Args:
      melody_event: A MonophonicMelody event value. -2 = no event,
          -1 = note-off event, [0, 127] = note-on event for that midi pitch.

    Returns:
      An int in the range [0, self._num_model_events). 0 = no event,
      1 = note-off event, [2, self._num_model_events) = note-on event for
      that pitch relative to the [self._min_note, self._max_note) range.
    """
    if melody_event < 0:
      return melody_event + NUM_SPECIAL_MELODY_EVENTS
    return melody_event - self.min_note + NUM_SPECIAL_MELODY_EVENTS

  def model_event_to_melody_event(self, model_event):
    """Expands a zero-based index value to its equivalent melody event value.

    Args:
      model_event: An int in the range [0, self._num_model_events).
          0 = no event, 1 = note-off event,
          [2, self._num_model_events) = note-on event for that pitch relative
          to the [self._min_note, self._max_note) range.

    Returns:
      A MonophonicMelody event value. -2 = no event, -1 = note-off event,
      [0, 127] = note-on event for that midi pitch.
    """
    if model_event < NUM_SPECIAL_MELODY_EVENTS:
      return model_event - NUM_SPECIAL_MELODY_EVENTS
    return model_event - NUM_SPECIAL_MELODY_EVENTS + self.min_note

  def events_to_input(self, events, position):
    """Returns the input vector for the given position in the melody.

    Returns a one-hot vector for the given position in the melody mapped to the
    model's event range. 0 = no event, 1 = note-off event,
    [2, self._num_model_events) = note-on event for that pitch relative to the
    [self._min_note, self._max_note) range.

    Args:
      events: A MonophonicMelody object.
      position: An integer event position in the melody.

    Returns:
      An input vector, a list of floats.
    """
    input_ = [0.0] * self.input_size
    input_[self.melody_event_to_model_event(events[position])] = 1.0
    return input_

  def events_to_label(self, events, position):
    """Returns the label for the given position in the melody.

    Returns the zero-based index value for the given position in the melody
    mapped to the model's event range. 0 = no event, 1 = note-off event,
    [2, self._num_model_events) = note-on event for that pitch relative to the
    [self._min_note, self._max_note) range.

    Args:
      events: A MonophonicMelody object.
      position: An integer event position in the melody.

    Returns:
      A label, an integer.
    """
    return self.melody_event_to_model_event(events[position])

  def class_index_to_event(self, class_index, events):
    """Returns the melody event for the given class index.

    This is the reverse process of the self.events_to_label method.

    Args:
      class_index: An integer in the range [0, self.num_classes).
      events: A MonophonicMelody object. This object is not used in this
          implementation.

    Returns:
      A MonophonicMelody event value.
    """
    return self.model_event_to_melody_event(class_index)
