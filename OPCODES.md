# Op-Code Legend

**Generated file — do not hand-edit.** Regenerate with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and this legend is *descriptive*, not prescriptive. Steps are pipe-delimited strings (`CODE|field|field|...`, at most 4 payload fields) built with `helpers.step()`; the final step of every problem is `Z|<final_answer>`.

247 distinct op-codes observed.

| Code | Payload fields | Example | Used by |
|---|---|---|---|
| `A` | 3 | `A\|25\|36\|61` | evaluate_expression_generator.py, fraction_op_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py, percent_word_problem_generator.py, polygon_perimeter_generator.py, pythag_hyp_generator.py, simple_stats_generator.py, temperature_conversion_generator.py |
| `ABS_CASE` | 2 | `ABS_CASE\|Case 1\|2x + 2 = 4` | absolute_value_equation_generator.py |
| `ABS_CHECK` | 2 | `ABS_CHECK\|-1 < 0\|Absolute value cannot be negative` | absolute_value_equation_generator.py |
| `ABS_INEQ_CHECK` | 2 | `ABS_INEQ_CHECK\|-3 < 0\|Absolute value is always non-negative` | absolute_value_inequality_generator.py |
| `ABS_INEQ_PART` | 2 | `ABS_INEQ_PART\|Part 1\|5x + 4 > 16 -> x > 12/5` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SETUP` | 1 | `ABS_INEQ_SETUP\|\|4x + 9\| < 13` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPECIAL` | 2 | `ABS_INEQ_SPECIAL\|c = 0\|Check logic for >` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPLIT` | 2 | `ABS_INEQ_SPLIT\|AND case\|-13 < 4x + 9 < 13` | absolute_value_inequality_generator.py |
| `ABS_SETUP` | 1 | `ABS_SETUP\|\|5x + 10\| = -1` | absolute_value_equation_generator.py |
| `ABS_SPLIT` | 2, 3 | `ABS_SPLIT\|Two cases\|2x + 2 = 4\|2x + 2 = -4` | absolute_value_equation_generator.py |
| `AB_ADD_DGT` | 3 | `AB_ADD_DGT\|col_0\|4+8+0\|12` | abacus_addition_generator.py |
| `AB_CARRY` | 3 | `AB_CARRY\|col_0\|1\|col_1` | abacus_addition_generator.py |
| `AB_CARRY_FINAL` | 1 | `AB_CARRY_FINAL\|1` | abacus_addition_generator.py |
| `AB_INFO` | 1 | `AB_INFO\|Adding 9828 column by column` | abacus_addition_generator.py |
| `AB_SET` | 1 | `AB_SET\|514` | abacus_addition_generator.py |
| `ADD_COL` | 3 | `ADD_COL\|col_1\|7+1+0\|->8 (carry 0)` | multi_digit_addition_generator.py |
| `ADD_PARTIALS` | 2 | `ADD_PARTIALS\|295292 + 3691150 + 51676100 + 516761000 + 738230000\|1310653542` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `ALIGN_NUM` | 2 | `ALIGN_NUM\|22977\|55918` | number_comparison_generator.py |
| `ANGLE_RELATION` | 1 | `ANGLE_RELATION\|4x + 13 = 3x + 20` | angle_relationships_generator.py |
| `ANGLE_SETUP` | 2 | `ANGLE_SETUP\|vertical\|Vertical angles are equal` | angle_relationships_generator.py |
| `ANGLE_SOLVE` | 2 | `ANGLE_SOLVE\|1x = 7\|x = 7` | angle_relationships_generator.py |
| `AREA` | 1, 3 | `AREA\|60` | geometry_area_perimeter_generator.py |
| `B` | 3 | `B\|38\|1\|381` | decimal_div_generator.py, long_division_generator.py, percent_problem_generator.py |
| `BORROW` | 3 | `BORROW\|col_1\|from_left\|1` | multi_digit_subtraction_generator.py |
| `C` | 3 | `C\|5/4\|20\|25/20` | fraction_comparison_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py |
| `CALC` | 1 | `CALC\|x = -10` | systems_elimination_generator.py, systems_substitution_generator.py |
| `CARRY_FINAL` | 1 | `CARRY_FINAL\|1` | multi_digit_addition_generator.py |
| `CHECK` | 3 | `CHECK\|cross_products\|2×24=48\|3×16=48` | ratio_table_generator.py |
| `CIRCLE_CALCULATE` | 2 | `CIRCLE_CALCULATE\|C = 10π\|10π` | circle_generator.py |
| `CIRCLE_FORMULA` | 1 | `CIRCLE_FORMULA\|C = 2πr` | circle_generator.py |
| `CIRCLE_SETUP` | 2 | `CIRCLE_SETUP\|5\|radius` | circle_generator.py |
| `CIRCLE_SUBSTITUTE` | 1 | `CIRCLE_SUBSTITUTE\|C = 2 × π × 5` | circle_generator.py |
| `CMP` | 3 | `CMP\|14/22\|33/22\|<` | fraction_comparison_generator.py, graph_interpret_generator.py |
| `CMP_NUM` | 3 | `CMP_NUM\|22977\|55918\|<` | number_comparison_generator.py |
| `COMB_CONST` | 3 | `COMB_CONST\|-9\|+6\|-3` | equation_from_two_points_generator.py, linear_complex_generator.py, simplify_expression_generator.py |
| `COMB_X` | 3 | `COMB_X\|-5x\|+3x\|-2x` | linear_complex_generator.py, simplify_expression_generator.py |
| `COMPOSITE_FACTOR` | 2 | `COMPOSITE_FACTOR\|2\|31` | divisibility_classification_generator.py |
| `COMP_INEQ_PART` | 2 | `COMP_INEQ_PART\|Part 1\|2x - 3 < -7 -> x < -2` | compound_inequality_generator.py |
| `COMP_INEQ_SETUP` | 1 | `COMP_INEQ_SETUP\|13 < x + 8 < 15` | compound_inequality_generator.py |
| `CONV_FACTOR` | 2 | `CONV_FACTOR\|1 ft\|12 in` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, unit_conversion_generator.py |
| `CONV_RESULT` | 2 | `CONV_RESULT\|8 ft\|96 in` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, temperature_conversion_generator.py, unit_conversion_generator.py |
| `COUNT_DP` | 3 | `COUNT_DP\|1\|2\|3` | decimal_mult_generator.py |
| `D` | 3 | `D\|632\|99\|6` | decimal_div_generator.py, dimensional_analysis_generator.py, geometry_area_perimeter_generator.py, linear_simple_generator.py, long_division_generator.py, order_of_operations_generator.py, percent_problem_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, rate_conversion_generator.py, ratio_table_generator.py, simple_probability_generator.py, slope_two_points_generator.py, temperature_conversion_generator.py |
| `DEC_ADD_COL` | 3 | `DEC_ADD_COL\|frac_0\|6+0+0\|->6 (carry 0)` | decimal_add_sub_generator.py |
| `DEC_ALIGN` | 2 | `DEC_ALIGN\|61.36\|04.30` | decimal_add_sub_generator.py |
| `DEC_CARRY_FINAL` | 1 | `DEC_CARRY_FINAL\|1` | decimal_add_sub_generator.py |
| `DEC_SHIFT` | 3 | `DEC_SHIFT\|57.7/8.0\|57.7/80\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `DEC_SUB_COL` | 3 | `DEC_SUB_COL\|frac_0\|4-2 (borrow_in 0)\|->2 (borrow_out 0)` | decimal_add_sub_generator.py |
| `DEC_TO_FRAC` | 2 | `DEC_TO_FRAC\|0.9\|9/10` | fraction_decimal_percent_converter.py |
| `DEC_TO_PERCENT` | 2 | `DEC_TO_PERCENT\|3.5\|350.00%` | fraction_decimal_percent_converter.py, percent_problem_generator.py |
| `DEC_TYPE` | 2 | `DEC_TYPE\|2/11\|repeating` | repeating_decimal_generator.py |
| `DEC_VALUE` | 2 | `DEC_VALUE\|2/11\|0.181818` | repeating_decimal_generator.py |
| `DISC` | 3 | `DISC\|9\|-40\|49` | quadratic_generator.py |
| `DIST` | 3 | `DIST\|-1\|-5x+1\|5x-1` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, simplify_expression_generator.py |
| `DIST_COMBINE` | 1 | `DIST_COMBINE\|-21y + -104 = 85` | systems_substitution_generator.py |
| `DIST_TERM` | 2 | `DIST_TERM\|3x\|- 12x^3 + 3x^2 + 6x` | multiplying_polynomials_generator.py |
| `DIV_CHECK` | 3 | `DIV_CHECK\|62\|2\|0` | divisibility_classification_generator.py |
| `DIV_COEFF` | 3 | `DIV_COEFF\|-3\|-2\|x=3/2` | linear_complex_generator.py |
| `DIV_SETUP` | 2 | `DIV_SETUP\|577\|80` | decimal_div_generator.py, percent_problem_generator.py |
| `E` | 3 | `E\|30\|2\|900` | pythag_hyp_generator.py |
| `EQ_2PT_SETUP` | 2 | `EQ_2PT_SETUP\|(-5, -10)\|(-7, -15)` | equation_from_two_points_generator.py |
| `EQ_OP_BOTH` | 4 | `EQ_OP_BOTH\|subtract\|7\|x\|3` | absolute_value_equation_generator.py, one_step_equation_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, two_step_equation_generator.py |
| `EQ_OP_NOTE` | 3 | `EQ_OP_NOTE\|add\|n\|to both sides` | equation_from_two_points_generator.py, literal_equation_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `EQ_RESULT` | 2 | `EQ_RESULT\|x\|3` | one_step_equation_generator.py, two_step_equation_generator.py |
| `EQ_SETUP` | 1 | `EQ_SETUP\|x = 120/5` | literal_equation_generator.py, one_step_equation_generator.py, proportion_word_problem_generator.py, standard_form_conversion_generator.py, two_step_equation_generator.py |
| `EQ_SIMPLIFY` | 1 | `EQ_SIMPLIFY\|9x = 72` | two_step_equation_generator.py |
| `EXP_EXPAND` | 1 | `EXP_EXPAND\|(-4) × (-4) × (-4)` | exponent_generator.py |
| `EXP_PARTIAL` | 3 | `EXP_PARTIAL\|-4\|-4\|16` | exponent_generator.py |
| `EXP_RULE_APPLY` | 4 | `EXP_RULE_APPLY\|subtract\|5\|2\|3` | exponent_generator.py |
| `EXP_RULE_IDENTIFY` | 2 | `EXP_RULE_IDENTIFY\|quotient_rule\|x^a / x^b = x^(a-b)` | exponent_generator.py |
| `EXP_RULE_SETUP` | 1 | `EXP_RULE_SETUP\|x^5 / x^2` | exponent_generator.py |
| `EXP_RULE_SIMPLIFY` | 1 | `EXP_RULE_SIMPLIFY\|x^3` | exponent_generator.py |
| `EXP_SETUP` | 2 | `EXP_SETUP\|-4\|3` | exponent_generator.py |
| `F` | 2 | `F\|3/6\|1/2` | fraction_op_generator.py, mixed_number_operation_generator.py, repeating_decimal_generator.py, simple_probability_generator.py, slope_two_points_generator.py |
| `FACT_CHECK` | 3 | `FACT_CHECK\|31\|1\|0` | factors_generator.py |
| `FACT_PAIR` | 2 | `FACT_PAIR\|1\|31` | factors_generator.py |
| `FIND_SLOPE` | 2 | `FIND_SLOPE\|Given slope (m1)\|2` | parallel_perpendicular_line_generator.py |
| `FOIL_F` | 2 | `FOIL_F\|First: (-9x) * (1x)\|-9x^2` | multiplying_binomials_generator.py |
| `FOIL_I` | 2 | `FOIL_I\|Inner: (7) * (1x)\|7x` | multiplying_binomials_generator.py |
| `FOIL_L` | 2 | `FOIL_L\|Last: (7) * (6)\|42` | multiplying_binomials_generator.py |
| `FOIL_O` | 2 | `FOIL_O\|Outer: (-9x) * (6)\|-54x` | multiplying_binomials_generator.py |
| `FOIL_SETUP` | 1 | `FOIL_SETUP\|(-9x + 7)(x + 6)` | multiplying_binomials_generator.py |
| `FRAC_TO_DEC` | 2 | `FRAC_TO_DEC\|7/10\|0.7` | fraction_decimal_percent_converter.py |
| `GCD_RESULT` | 1 | `GCD_RESULT\|1` | lcm_generator.py |
| `GCD_START` | 2 | `GCD_START\|75\|134` | gcf_generator.py, lcm_generator.py |
| `GCD_STEP` | 3 | `GCD_STEP\|75\|134\|75` | gcf_generator.py, lcm_generator.py |
| `GOAL` | 1 | `GOAL\|Convert to Slope-Intercept Form (y = mx + b)` | point_slope_generator.py, standard_form_conversion_generator.py |
| `GRAPH_CHANGE` | 3 | `GRAPH_CHANGE\|2018\|2019\|-3` | graph_interpret_generator.py |
| `GRAPH_DATA` | 2 | `GRAPH_DATA\|bar_chart\|Soccer:5,Tennis:44,Basketball:8,Swimming:46` | graph_interpret_generator.py |
| `GRAPH_MAX` | 2 | `GRAPH_MAX\|Week 7\|16` | graph_interpret_generator.py |
| `GRAPH_MAX_CHANGE` | 3 | `GRAPH_MAX_CHANGE\|2022\|2023\|8` | graph_interpret_generator.py |
| `GRAPH_MIN` | 2 | `GRAPH_MIN\|Math\|10` | graph_interpret_generator.py |
| `GRAPH_READ` | 2 | `GRAPH_READ\|Tennis\|44` | graph_interpret_generator.py |
| `I` | 2 | `I\|3/2\|2/3` | fraction_op_generator.py, mixed_number_operation_generator.py |
| `IMPROPER_TO_MIX` | 2 | `IMPROPER_TO_MIX\|486/35\|13 31/35` | mixed_number_operation_generator.py |
| `INEQ_FLIP` | 1 | `INEQ_FLIP\|Multiplying by negative number reverses inequality` | one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_OP_ALL` | 3 | `INEQ_OP_ALL\|subtract\|9\|-22 < 4x < 4` | absolute_value_inequality_generator.py, compound_inequality_generator.py |
| `INEQ_OP_BOTH` | 4 | `INEQ_OP_BOTH\|subtract\|1\|x\|-10` | one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_RESULT` | 3 | `INEQ_RESULT\|x\|<\|-10` | one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SETUP` | 1 | `INEQ_SETUP\|x + 1 < -9` | one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SIMPLIFY` | 1 | `INEQ_SIMPLIFY\|-4x ≥ 8` | two_step_inequality_generator.py |
| `INT_ABS` | 2 | `INT_ABS\|-14\|14` | integer_operations_generator.py |
| `INT_ALIGN` | 2 | `INT_ALIGN\|36767\|33851` | multi_digit_addition_generator.py, multi_digit_subtraction_generator.py |
| `INT_APPLY_SIGN` | 3 | `INT_APPLY_SIGN\|12\|negative\|-12` | integer_operations_generator.py |
| `INT_OP` | 4 | `INT_OP\|-\|14\|2\|12` | integer_operations_generator.py |
| `INT_REWRITE` | 2 | `INT_REWRITE\|-14 - (-2)\|-14 + 2` | integer_operations_generator.py |
| `INT_SIGN_RULE` | 2 | `INT_SIGN_RULE\|subtract_rule\|Subtracting is adding the opposite` | integer_operations_generator.py |
| `L` | 3 | `L\|4\|5\|20` | fraction_comparison_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py |
| `LCM_FROM_GCD` | 3 | `LCM_FROM_GCD\|113*20\|1\|2260` | lcm_generator.py |
| `LINE_RELATION_SETUP` | 3 | `LINE_RELATION_SETUP\|parallel\|y = 2x + 2\|(-7, 2)` | parallel_perpendicular_line_generator.py |
| `M` | 2, 3 | `M\|6\|99\|594` | decimal_div_generator.py, dimensional_analysis_generator.py, evaluate_expression_generator.py, fraction_op_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, long_division_generator.py, mixed_number_operation_generator.py, multi_step_unit_conversion_generator.py, order_of_operations_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, rate_conversion_generator.py, ratio_table_generator.py, temperature_conversion_generator.py, unit_conversion_generator.py, volume_rect_prism_generator.py |
| `MEAN_DIV` | 3 | `MEAN_DIV\|68\|7\|9.714285714285714` | simple_stats_generator.py |
| `MEDIAN_PAIR` | 2 | `MEDIAN_PAIR\|7\|9` | simple_stats_generator.py |
| `MEDIAN_PICK` | 3 | `MEDIAN_PICK\|5\|\|5` | simple_stats_generator.py |
| `MIX_IMPROPER` | 2 | `MIX_IMPROPER\|3 6/7\|27/7` | mixed_number_operation_generator.py |
| `MODE` | 2 | `MODE\|1\|2, 3, 6, 11, 13, 14, 16, 20` | simple_stats_generator.py |
| `MODE_COUNT` | 2 | `MODE_COUNT\|2\|1` | simple_stats_generator.py |
| `MONO_ADD_EXP` | 2 | `MONO_ADD_EXP\|x^8 * x^4 = x^(8+4)\|x^12` | monomial_mult_div_generator.py |
| `MONO_DIV_COEFF` | 2 | `MONO_DIV_COEFF\|-36 / -4\|9` | monomial_mult_div_generator.py |
| `MONO_MULT_COEFF` | 2 | `MONO_MULT_COEFF\|7 * 2\|14` | monomial_mult_div_generator.py |
| `MONO_SETUP` | 1 | `MONO_SETUP\|(7x^8)(2x^4)` | monomial_mult_div_generator.py |
| `MONO_SUB_EXP` | 2 | `MONO_SUB_EXP\|x^2 / x^2 = x^(2-2)\|x^0 = 1` | monomial_mult_div_generator.py |
| `MOVE_TERM` | 3 | `MOVE_TERM\|-3x\|left\|-5x-6+3x = -9` | linear_complex_generator.py, standard_form_conversion_generator.py |
| `MUL_PARTIAL` | 3 | `MUL_PARTIAL\|4\|73823\|295292` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_SETUP` | 2 | `MUL_SETUP\|73823\|17754` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `NEW_SLOPE` | 2 | `NEW_SLOPE\|New slope (m2) = 2\|Parallel lines have the same slope` | parallel_perpendicular_line_generator.py |
| `PARALLEL_RELATION` | 1 | `PARALLEL_RELATION\|2x + 29 = 5x - 25` | angle_relationships_generator.py |
| `PARALLEL_SETUP` | 2 | `PARALLEL_SETUP\|corresponding\|Corresponding angles are equal` | angle_relationships_generator.py |
| `PARALLEL_SOLVE` | 2 | `PARALLEL_SOLVE\|-3x = -54\|x = 18` | angle_relationships_generator.py |
| `PERCENT_CALC_PART` | 3 | `PERCENT_CALC_PART\|0.75\|120\|90` | percent_problem_generator.py |
| `PERCENT_TO_DEC` | 2 | `PERCENT_TO_DEC\|90%\|0.9` | fraction_decimal_percent_converter.py, percent_problem_generator.py, percent_word_problem_generator.py |
| `PERIM` | 1 | `PERIM\|26` | geometry_area_perimeter_generator.py, polygon_perimeter_generator.py |
| `PF_PRIME` | 1 | `PF_PRIME\|3` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PF_STEP` | 3 | `PF_STEP\|72\|2\|36` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PICTO_COUNT` | 2 | `PICTO_COUNT\|Giraffes\|2` | graph_interpret_generator.py |
| `PICTO_KEY` | 2 | `PICTO_KEY\|■\|5` | graph_interpret_generator.py |
| `PLACE_DP` | 3 | `PLACE_DP\|2760333\|3\|2760.333` | decimal_mult_generator.py |
| `PLACE_DP_Q` | 2 | `PLACE_DP_Q\|72125\|2` | decimal_div_generator.py, percent_problem_generator.py |
| `POINT_SLOPE_SETUP` | 1 | `POINT_SLOPE_SETUP\|y + 10 = 5/2(x + 5)` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py |
| `POLY_COMBINE` | 1 | `POLY_COMBINE\|-x + 7` | multiplying_binomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_DIST_NEG` | 1 | `POLY_DIST_NEG\|Distribute negative sign to second polynomial` | polynomial_add_sub_generator.py |
| `POLY_DIV_SETUP` | 1 | `POLY_DIV_SETUP\|(15x^3 - 6x) / (-3x)` | polynomial_div_monomial_generator.py |
| `POLY_DIV_SPLIT` | 1 | `POLY_DIV_SPLIT\|(15x^3) / (-3x) + (-6x) / (-3x)` | polynomial_div_monomial_generator.py |
| `POLY_GROUP_LIKE` | 1 | `POLY_GROUP_LIKE\|(2x -3x) + (2 +5)` | multiplying_polynomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_MULT_SETUP` | 1 | `POLY_MULT_SETUP\|(3x - 4)(-4x^2 + x + 2)` | multiplying_polynomials_generator.py |
| `POLY_SETUP` | 1 | `POLY_SETUP\|(2x + 2) - (3x - 5)` | polynomial_add_sub_generator.py |
| `PRIME` | 1 | `PRIME\|37` | divisibility_classification_generator.py |
| `PROB_CONDITIONAL` | 2 | `PROB_CONDITIONAL\|P(blue\|first was red)\|4/9` | compound_probability_generator.py |
| `PROB_DEPENDENT` | 1 | `PROB_DEPENDENT\|Drawing without replacement means dependent events` | compound_probability_generator.py |
| `PROB_DESCRIBE` | 1 | `PROB_DESCRIBE\|Two coin flips, looking for heads then tails` | compound_probability_generator.py |
| `PROB_IDENTIFY` | 2 | `PROB_IDENTIFY\|P(heads)\|1/2` | compound_probability_generator.py |
| `PROB_INDEPENDENT` | 1 | `PROB_INDEPENDENT\|Coin flips are independent events` | compound_probability_generator.py |
| `PROB_MULTIPLY` | 3 | `PROB_MULTIPLY\|1/2\|1/2\|1/4` | compound_probability_generator.py |
| `PROB_SETUP` | 2 | `PROB_SETUP\|1\|7` | simple_probability_generator.py |
| `PROB_SIMPLIFY` | 2 | *(not observed in sampling)* | compound_probability_generator.py |
| `PROP_SETUP` | 1 | `PROP_SETUP\|15/5 = x/8` | proportion_word_problem_generator.py, proportional_relationship_generator.py |
| `PYTHAG_CALCULATE` | 2 | `PYTHAG_CALCULATE\|d² = 256 + 900 = 1156\|1156` | pythag_leg_generator.py |
| `PYTHAG_CONTEXT` | 2 | `PYTHAG_CONTEXT\|displacement\|east=16m, north=30m` | pythag_leg_generator.py |
| `PYTHAG_FORMULA` | 1 | `PYTHAG_FORMULA\|a² + b² = c²` | pythag_leg_generator.py |
| `PYTHAG_MODEL` | 3 | `PYTHAG_MODEL\|east=16\|north=30\|distance=?` | pythag_leg_generator.py |
| `PYTHAG_ROOT` | 2 | `PYTHAG_ROOT\|1225\|35` | pythag_leg_generator.py |
| `PYTHAG_SETUP` | 3 | `PYTHAG_SETUP\|c=37\|a=12\|b=?` | pythag_leg_generator.py |
| `PYTHAG_SOLVE` | 2 | `PYTHAG_SOLVE\|b² = 1369 - 144\|1225` | pythag_leg_generator.py |
| `PYTHAG_SQUARE` | 2 | `PYTHAG_SQUARE\|12\|144` | pythag_leg_generator.py |
| `PYTHAG_SUBSTITUTE` | 1 | `PYTHAG_SUBSTITUTE\|12² + b² = 37²` | pythag_leg_generator.py |
| `Q1` | 4 | `Q1\|3\|7\|2\|5` | quadratic_generator.py |
| `Q2` | 4 | `Q2\|3\|7\|2\|-2` | quadratic_generator.py |
| `R` | 1 | `R\|28` | long_division_generator.py |
| `RATIO_BASE` | 3 | `RATIO_BASE\|2:3\|1\|2:3` | ratio_table_generator.py |
| `RATIO_TABLE` | 2 | `RATIO_TABLE\|Red (liters): 2, 12, 16, 22\|Blue (liters): 3, 18, ?, 33` | ratio_table_generator.py |
| `REARRANGE_EQ` | 1 | `REARRANGE_EQ\|whole = 60 / 0.4` | percent_problem_generator.py |
| `REWRITE` | 1 | `REWRITE\|12 + 36` | evaluate_expression_generator.py, linear_complex_generator.py, literal_equation_generator.py, order_of_operations_generator.py, simplify_expression_generator.py, standard_form_conversion_generator.py |
| `ROOT` | 2 | `ROOT\|1156\|34` | pythag_hyp_generator.py, quadratic_generator.py |
| `ROOT_EXTRACT` | 2 | `ROOT_EXTRACT\|2` | exponent_generator.py |
| `ROOT_IDENTIFY` | 3 | `ROOT_IDENTIFY\|8\|perfect_cube\|2` | exponent_generator.py |
| `ROOT_SETUP` | 1 | `ROOT_SETUP\|∛8` | exponent_generator.py |
| `ROOT_SIMPLIFY` | 1 | `ROOT_SIMPLIFY\|5√7` | exponent_generator.py |
| `ROUND_CHECK` | 3 | `ROUND_CHECK\|93155\|10\|>=5` | place_value_rounding_generator.py |
| `ROUND_RESULT` | 2 | `ROUND_RESULT\|93155\|93160` | place_value_rounding_generator.py |
| `S` | 3 | `S\|632\|594\|38` | decimal_div_generator.py, fraction_op_generator.py, graph_interpret_generator.py, linear_simple_generator.py, long_division_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, slope_two_points_generator.py, temperature_conversion_generator.py |
| `SA_BASES` | 2 | `SA_BASES\|2π(8)² = 2π × 64\|128π` | volume_3d_generator.py |
| `SA_FACES` | 3 | `SA_FACES\|top/bottom\|9 × 12\|108` | volume_3d_generator.py |
| `SA_FORMULA` | 1 | `SA_FORMULA\|SA = 2(lw + lh + wh)` | volume_3d_generator.py |
| `SA_LATERAL` | 2 | `SA_LATERAL\|2π × 8 × 5\|80π` | volume_3d_generator.py |
| `SA_SETUP` | 2 | `SA_SETUP\|rectangular_prism\|l=9, w=12, h=7` | volume_3d_generator.py |
| `SA_TOTAL` | 2 | `SA_TOTAL\|SA = 2(108 + 63 + 84)\|510` | volume_3d_generator.py |
| `SCALE_DIV` | 3 | `SCALE_DIV\|60\|10\|6.0` | scaling_generator.py |
| `SCALE_IDENTIFY` | 2 | `SCALE_IDENTIFY\|0.5 centimeters\|actual_dimension` | scaling_generator.py |
| `SCALE_MULT` | 3 | `SCALE_MULT\|0.5\|20\|10.0` | scaling_generator.py |
| `SCALE_SETUP` | 3 | `SCALE_SETUP\|1 centimeter\|20 meters\|20` | scaling_generator.py |
| `SCI_IDENTIFY` | 2 | `SCI_IDENTIFY\|8.1\|2` | exponent_generator.py |
| `SCI_MOVE_DECIMAL` | 2 | `SCI_MOVE_DECIMAL\|right\|2` | exponent_generator.py |
| `SCI_OPERATION` | 4 | `SCI_OPERATION\|multiply_coefficients\|2.4\|4.9\|11.76` | exponent_generator.py |
| `SCI_SETUP` | 1 | `SCI_SETUP\|(2.4 × 10^6) × (4.9 × 10^2)` | exponent_generator.py |
| `SETUP_PERCENT_EQ` | 1 | `SETUP_PERCENT_EQ\|part = 0.75 * 120` | percent_problem_generator.py |
| `SIMILAR_APPLY` | 3 | `SIMILAR_APPLY\|5\|3\|15` | scaling_generator.py |
| `SIMILAR_SCALE` | 3 | `SIMILAR_SCALE\|15\|5\|3` | scaling_generator.py |
| `SIMILAR_SETUP` | 3 | `SIMILAR_SETUP\|triangle\|5,5,9\|15 (others unknown)` | scaling_generator.py |
| `SLOPE_CALC` | 2 | *(not observed in sampling)* | equation_from_two_points_generator.py |
| `SLOPE_FORMULA` | 1 | `SLOPE_FORMULA\|m = (y2 - y1) / (x2 - x1)` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_INT_IDENTIFY` | 2 | `SLOPE_INT_IDENTIFY\|Slope (m)\|1` | slope_intercept_form_generator.py |
| `SLOPE_INT_MATCH` | 2 | `SLOPE_INT_MATCH\|Compare to Slope-Intercept Form\|y = mx + b` | slope_intercept_form_generator.py |
| `SLOPE_INT_SETUP` | 1 | `SLOPE_INT_SETUP\|y = x` | slope_intercept_form_generator.py |
| `SLOPE_RESULT` | 1 | `SLOPE_RESULT\|5/2` | equation_from_two_points_generator.py |
| `SLOPE_SETUP` | 2 | `SLOPE_SETUP\|(10, 8)\|(9, 5)` | slope_two_points_generator.py |
| `SLOPE_SUBST` | 1 | `SLOPE_SUBST\|m = (5 - 8) / (9 - 10)` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_UNDEFINED` | 1 | `SLOPE_UNDEFINED\|Division by zero` | slope_two_points_generator.py |
| `SORT` | 2 | `SORT\|5,17,20,3,9,13,1\|1,3,5,9,13,17,20` | simple_stats_generator.py |
| `STAT_ABS_DEV` | 2 | `STAT_ABS_DEV\|9\|9` | statistics_generator.py |
| `STAT_AVERAGE` | 2 | `STAT_AVERAGE\|(52 + 58) / 2\|55.0` | statistics_generator.py |
| `STAT_COUNT` | 1 | `STAT_COUNT\|7` | statistics_generator.py |
| `STAT_DEVIATION` | 3 | `STAT_DEVIATION\|57\|48\|9` | statistics_generator.py |
| `STAT_DIVIDE` | 2 | `STAT_DIVIDE\|385 / 7\|55` | statistics_generator.py |
| `STAT_FREQUENCY` | 2 | `STAT_FREQUENCY\|32\|3` | statistics_generator.py |
| `STAT_MAD` | 3 | `STAT_MAD\|68\|5\|13.6` | statistics_generator.py |
| `STAT_MAX` | 1 | `STAT_MAX\|89` | statistics_generator.py |
| `STAT_MEAN` | 2 | `STAT_MEAN\|240 / 5\|48` | statistics_generator.py |
| `STAT_MIDDLE` | 2 | `STAT_MIDDLE\|positions 4 and 5\|52, 58` | statistics_generator.py |
| `STAT_MIN` | 1 | `STAT_MIN\|48` | statistics_generator.py |
| `STAT_MODE` | 2 | `STAT_MODE\|50 and 72\|4` | statistics_generator.py |
| `STAT_ORDER` | 1 | `STAT_ORDER\|28, 37, 41, 52, 58, 81, 92, 96` | statistics_generator.py |
| `STAT_RANGE` | 2 | `STAT_RANGE\|89 - 48\|41` | statistics_generator.py |
| `STAT_SETUP` | 1 | `STAT_SETUP\|38, 49, 56, 53, 80, 45, 64` | statistics_generator.py |
| `STAT_SUM` | 2 | `STAT_SUM\|38 + 49 + 56 + 53 + 80 + 45 + 64\|385` | statistics_generator.py |
| `SUBST` | 3 | `SUBST\|x\|1\|3(1)-5y-9` | evaluate_expression_generator.py |
| `SUB_COL` | 3 | `SUB_COL\|col_1\|1-6-borrow0\|->5 (borrow_out 1)` | multi_digit_subtraction_generator.py |
| `SYS_ADD` | 1 | `SYS_ADD\|Add equations: 18x = 72` | systems_elimination_generator.py |
| `SYS_EQ_NEW` | 1 | `SYS_EQ_NEW\|New equation with y only` | systems_substitution_generator.py |
| `SYS_ISOLATE` | 2 | `SYS_ISOLATE\|Isolate x in Eq 1\|x = 4y + 26` | systems_substitution_generator.py |
| `SYS_MULT` | 1 | `SYS_MULT\|Eq1 * -3, Eq2 * -1` | systems_elimination_generator.py |
| `SYS_REWRITE` | 2 | `SYS_REWRITE\|15x + 12y = -60\|3x - 12y = 132` | systems_elimination_generator.py |
| `SYS_SETUP` | 2 | `SYS_SETUP\|x - 4y = 26\|-4x -5y = 85` | systems_elimination_generator.py, systems_substitution_generator.py |
| `SYS_SUBST` | 1 | `SYS_SUBST\|Substitute x in Eq 2` | systems_substitution_generator.py |
| `SYS_SUBST_BACK` | 1 | `SYS_SUBST_BACK\|Substitute y=-9 into x = 4y + 26` | systems_elimination_generator.py, systems_substitution_generator.py |
| `TRI_ANGLE_SETUP` | 3 | `TRI_ANGLE_SETUP\|46\|54\|exterior` | angle_relationships_generator.py |
| `TRI_ANGLE_SOLVE` | 2 | `TRI_ANGLE_SOLVE\|exterior = 46 + 54\|100` | angle_relationships_generator.py |
| `TRI_ANGLE_SUM` | 1 | `TRI_ANGLE_SUM\|Exterior angle = sum of remote interior angles` | angle_relationships_generator.py |
| `UNIT_RATE_DIV` | 3 | `UNIT_RATE_DIV\|$1.50\|3\|$0.50` | unit_rate_generator.py |
| `UNIT_RATE_PICK` | 2 | `UNIT_RATE_PICK\|7\|70` | unit_rate_generator.py |
| `UNIT_RATE_SETUP` | 3 | `UNIT_RATE_SETUP\|3\|tickets\|$1.50` | unit_rate_generator.py |
| `UNIT_RATE_TABLE` | 2 | `UNIT_RATE_TABLE\|7,9,10\|70,90,100` | unit_rate_generator.py |
| `VOLUME` | 1 | `VOLUME\|208` | volume_rect_prism_generator.py |
| `VOL_BASE_AREA` | 2 | `VOL_BASE_AREA\|Base Area = (1/2) × 11 × 4\|22.0` | volume_3d_generator.py |
| `VOL_CALCULATE` | 2 | `VOL_CALCULATE\|V = 6 × 8 × 7\|336` | volume_3d_generator.py |
| `VOL_FORMULA` | 1 | `VOL_FORMULA\|V = l × w × h` | volume_3d_generator.py |
| `VOL_SETUP` | 2 | `VOL_SETUP\|rectangular_prism\|l=6, w=8, h=7` | volume_3d_generator.py |
| `Z` | 1 | `Z\|63 R84` | abacus_addition_generator.py, absolute_value_equation_generator.py, absolute_value_inequality_generator.py, angle_relationships_generator.py, circle_generator.py, compound_inequality_generator.py, compound_probability_generator.py, decimal_add_sub_generator.py, decimal_div_generator.py, decimal_mult_generator.py, dimensional_analysis_generator.py, divisibility_classification_generator.py, equation_from_two_points_generator.py, evaluate_expression_generator.py, exponent_generator.py, factors_generator.py, fraction_comparison_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, gcf_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, integer_operations_generator.py, lcm_generator.py, linear_complex_generator.py, linear_simple_generator.py, literal_equation_generator.py, long_division_generator.py, mixed_number_operation_generator.py, monomial_mult_div_generator.py, multi_digit_addition_generator.py, multi_digit_multiplication_generator.py, multi_digit_subtraction_generator.py, multi_step_unit_conversion_generator.py, multiplying_binomials_generator.py, multiplying_polynomials_generator.py, number_comparison_generator.py, one_step_equation_generator.py, one_step_inequality_generator.py, order_of_operations_generator.py, parallel_perpendicular_line_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, place_value_rounding_generator.py, point_slope_generator.py, polygon_perimeter_generator.py, polynomial_add_sub_generator.py, polynomial_div_monomial_generator.py, prime_factorization_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, pythag_hyp_generator.py, pythag_leg_generator.py, quadratic_generator.py, rate_conversion_generator.py, ratio_table_generator.py, repeating_decimal_generator.py, scaling_generator.py, simple_probability_generator.py, simple_stats_generator.py, simplify_expression_generator.py, slope_intercept_form_generator.py, slope_two_points_generator.py, standard_form_conversion_generator.py, statistics_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, temperature_conversion_generator.py, two_step_equation_generator.py, two_step_inequality_generator.py, unit_conversion_generator.py, unit_rate_generator.py, volume_3d_generator.py, volume_rect_prism_generator.py |
