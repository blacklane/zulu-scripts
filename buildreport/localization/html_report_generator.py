#!/usr/bin/python

from strings_resources_comparator import STRINGS_ADDED_IN_FIRST_FILE
from strings_resources_comparator import STRINGS_ADDED_IN_SECOND_FILE
from strings_resources_comparator import SAME_KEY_DIFFERENT_VALUES

TABLE = "<table border=1>\n"
CTABLE = "</table>\n"
TR = "<tr>"
CTR = "</tr>\n"
TH = '<th align="left">'
TH_COLSPAN_2 = '<th align="left" colspan="2">'
TH_COLSPAN_3 = '<th align="left" colspan="3">'
CTH = "</th>\n"
TD = "<td>"
TD_COLSPAN_2 = '<td colspan="2">'
CTD = "</td>\n"
BR = "<br>\n"
FONT_WHITE = '<font color="#fff">'
CFONT = "</font>"


##
# Generates html tables which contain result report.
#
# @param locale_keys See localization_report.py
# @param result A dictionary with result which is generated by localization_report.py
#
# @return A string which contains generated html.
def generate_report(locale_keys, result):
  str_list = []
  for locale_key in locale_keys:
    _phraseapp_diff_table(str_list, locale_key, result[locale_key])
    str_list.extend([BR, BR])

  # If result key is not in locale keys then it's the result of locale files comparision.
  for result_item in result.items():
    if result_item[0] not in locale_keys:
      _localization_diff_table(str_list, result_item[0], result_item[1])
      str_list.extend([BR, BR])

  return u' '.join(str_list).encode('utf-8')


def _phraseapp_diff_table(str_list, locale_key, result_for_locale):
  str_list.append(TABLE)
  str_list.extend([TR, TH_COLSPAN_3, locale_key, CTH, CTR])

  _add_subtable_with_added_keys(str_list, "Keys added in the app", result_for_locale[STRINGS_ADDED_IN_FIRST_FILE])
  _add_space(str_list)
  _add_subtable_with_added_keys(str_list, "Keys added on PhraseApp", result_for_locale[STRINGS_ADDED_IN_SECOND_FILE])
  _add_space(str_list)
  _add_subtable_with_new_values(str_list, "Keys with different values", result_for_locale[SAME_KEY_DIFFERENT_VALUES])

  str_list.append(CTABLE)


def _add_subtable_with_added_keys(str_list, title, content_dict):
  str_list.extend([TR, TH_COLSPAN_3, title, CTH, CTR])
  for string_entry in content_dict.items():
    str_list.extend([TR, TD, string_entry[0], CTD, TD_COLSPAN_2, string_entry[1], CTD, CTR])


def _add_subtable_with_new_values(str_list, title, content_dict):
  str_list.extend([TR, TH_COLSPAN_3, title, CTH, CTR])
  str_list.extend([TR, TH, "Key", CTH, TH, "In the app", CTH, TH, "On PhraseApp", CTH, CTR])

  for string_entry in content_dict.items():
    string_key = string_entry[0]
    string_values_pair = string_entry[1]
    str_list.extend([TR, TD, string_key, CTD, TD, string_values_pair[0], CTD, TD, string_values_pair[1], CTD, CTR])


def _localization_diff_table(str_list, compared_locales, content_dict):
  str_list.append(TABLE)
  str_list.extend([TR, TH_COLSPAN_2, compared_locales, CTH, CTR])
  _add_colored_subtable_for_diff_table(str_list, content_dict[STRINGS_ADDED_IN_FIRST_FILE], "green")
  _add_colored_subtable_for_diff_table(str_list, content_dict[STRINGS_ADDED_IN_SECOND_FILE], "darkred")

  str_list.append(CTABLE)


def _add_colored_subtable_for_diff_table(str_list, content_dict, color):
  for string_entry in content_dict.items():
    str_list.extend([_colored_tr(color), TD, FONT_WHITE, string_entry[0], CFONT, CTD,
                     TD, FONT_WHITE, string_entry[1], CFONT, CTD, CTR])


def _add_space(str_list):
  str_list.extend([_colored_tr("lightgray"), TH_COLSPAN_3, BR, CTH, CTR])


def _colored_tr(color):
  return '<tr style="background:' + color + '">'
