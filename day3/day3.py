from enum import Enum

FILENAME = './input.txt'

MULTIPLICATION_SUM = 0

MUL_PREFIX = 'mul('
DO_STRING = 'do()'
DONT_STRING = 'don\'t()'

class Parsing(Enum):
  PREFIX = 1
  FIRST_NUM = 2
  SECOND_NUM = 3


class Parser(object):

  def __init__(self, allow_multiplication_toggle = False):
    self.multiplication_sum = 0
    self.mul_prefix_index = 0
    self.do_string_match_index = 0
    self.dont_string_match_index = 0
    self.stage = Parsing.PREFIX
    self.first_num_str_array = []
    self.first_num = None
    self.second_num_str_array = []
    self.second_num = None
    self.enable_multiplication = True
    self.allow_multiplication_toggle = allow_multiplication_toggle

  def reset_parser(self):
    self.stage = Parsing.PREFIX
    self.mul_prefix_index = 0
    self.first_num_str_array.clear()
    self.first_num = None
    self.second_num_str_array.clear()
    self.second_num = None


  # TODO(derekwu): refactor this into helper functions for easier
  # readability
  def parse_line(self, line):
    for char in line:
      if self.allow_multiplication_toggle:
        if not self.enable_multiplication:
          # we're solely looking for do() enabling
          if char == DO_STRING[self.do_string_match_index]:
            self.do_string_match_index += 1
            if self.do_string_match_index == len(DO_STRING):
              self.enable_multiplication = True
              self.do_string_match_index = 0
            continue
          else:
            self.do_string_match_index = 0
            continue
        # else multiplication is enabled (note that all paths continue in
        # above code, so the else is implied. This needs to be refactored)

        # check for don't()
        if char == DONT_STRING[self.dont_string_match_index]:
          # We are now matching to the don't string, so any previous progress
          # on multiplication needs to be reset
          # TODO(derekwu): write a check to only reset on first match of don't string
          self.reset_parser()
          self.dont_string_match_index += 1

          if self.dont_string_match_index == len(DONT_STRING):
            self.enable_multiplication = False
            self.dont_string_match_index = 0
          continue
        else:
          self.dont_string_match_index = 0
          # Do not continue here as we need to check if the same char matches mul


      if self.stage == Parsing.PREFIX:
        # In this stage we are looking for a mul() prefix match
        if char == MUL_PREFIX[self.mul_prefix_index]:
          self.mul_prefix_index += 1
          if self.mul_prefix_index == len(MUL_PREFIX):
            # We have completed the prefix match, we will start
            # parsing the first number starting with the next character
            self.stage = Parsing.FIRST_NUM
          continue
        else: # char does not match prefix, reset and try again
          self.reset_parser()
          continue

      if self.stage == Parsing.FIRST_NUM:
        if len(self.first_num_str_array) and char == ',':
          # We have finished parsing the first number, start
          # parsing second number
          self.first_num = int(''.join(self.first_num_str_array))
          self.stage = Parsing.SECOND_NUM
          continue
        elif char.isdigit():
          self.first_num_str_array.append(char)
          continue
        else: # invalid character, reset everything and return to prefix parsing
          self.reset_parser()
          continue
      if self.stage == Parsing.SECOND_NUM:
        if len(self.second_num_str_array) and char == ')':
          # we have finished parsing the second number. Save multiplication
          # and reset parser
          self.second_num = int(''.join(self.second_num_str_array))
          self.multiplication_sum += self.first_num * self.second_num
          self.reset_parser()
          continue
        elif char.isdigit():
          self.second_num_str_array.append(char)
          continue
        else: # invalid character, reset everything and return to prefix parsing
          self.reset_parser()
          continue

  def get_multiplication_sum(self):
    return self.multiplication_sum



def parse_file_by_line(filename, parser):
	with open(filename, 'r') as f:
		for line in f:
			parser.parse_line(line)

if __name__=="__main__":
  parser = Parser()

  parse_file_by_line(FILENAME, parser)
  print('PART 1')
  print(parser.get_multiplication_sum())

  second_parser = Parser(allow_multiplication_toggle=True)
  parse_file_by_line(FILENAME, second_parser)


  print('PART 2')
  print(second_parser.get_multiplication_sum())

