# Op-Code Legend

**Generated file — do not hand-edit.** Regenerate with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and this legend is *descriptive*, not prescriptive. Steps are pipe-delimited strings (`CODE|field|field|...`, at most 4 payload fields) built with `helpers.step()`; the final step of every problem is `Z|<final_answer>`.

503 distinct op-codes observed.

| Code | Payload fields | Example | Used by |
|---|---|---|---|
| `A` | 3 | `A\|27\|2\|29` | angle_measure_generator.py, arithmetic_sequence_generator.py, base_conversion_generator.py, binomial_probability_generator.py, chi_square_generator.py, circle_equation_generator.py, complex_division_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, curve_analysis_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, determinant_generator.py, distance_formula_generator.py, dot_product_generator.py, ellipse_features_generator.py, euler_characteristic_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finance_generator.py, five_number_summary_generator.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, geometric_mean_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, hypercube_counting_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, nets_surface_area_generator.py, order_of_operations_generator.py, parabola_features_generator.py, pascal_triangle_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, polygon_perimeter_generator.py, polynomial_zeros_generator.py, probability_addition_rule_generator.py, pythag_hyp_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, regression_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, round_solids_generator.py, segment_partition_generator.py, sigma_notation_generator.py, simple_stats_generator.py, standard_deviation_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py, z_score_generator.py |
| `ABS_CASE` | 2 | `ABS_CASE\|Case 1\|5x + 2 = 10` | absolute_value_equation_generator.py |
| `ABS_CHECK` | 2 | `ABS_CHECK\|-1 < 0\|Absolute value cannot be negative` | absolute_value_equation_generator.py |
| `ABS_INEQ_CHECK` | 2 | `ABS_INEQ_CHECK\|-3 < 0\|Absolute value cannot be negative` | absolute_value_inequality_generator.py |
| `ABS_INEQ_PART` | 2 | `ABS_INEQ_PART\|Part 1\|x + 1 > 16 -> x > 15` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SETUP` | 1 | `ABS_INEQ_SETUP\|\|x + 1\| > 16` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPECIAL` | 2 | `ABS_INEQ_SPECIAL\|c = 0\|Check logic for >` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPLIT` | 2 | `ABS_INEQ_SPLIT\|OR case\|x + 1 > 16 OR x + 1 < -16` | absolute_value_inequality_generator.py |
| `ABS_SETUP` | 1 | `ABS_SETUP\|\|5x + 2\| = 10` | absolute_value_equation_generator.py |
| `ABS_SPLIT` | 2, 3 | `ABS_SPLIT\|Two cases\|5x + 2 = 10\|5x + 2 = -10` | absolute_value_equation_generator.py |
| `ABS_VAL` | 2 | `ABS_VAL\|(-5)\|5` | taxicab_geometry_generator.py |
| `AB_ADD_DGT` | 3 | `AB_ADD_DGT\|col_0\|0+1+0\|1` | abacus_addition_generator.py |
| `AB_CARRY` | 3 | `AB_CARRY\|col_1\|1\|col_2` | abacus_addition_generator.py |
| `AB_CARRY_FINAL` | 1 | `AB_CARRY_FINAL\|1` | abacus_addition_generator.py |
| `AB_INFO` | 1 | `AB_INFO\|Adding 4581 column by column` | abacus_addition_generator.py |
| `AB_SET` | 1 | `AB_SET\|5230` | abacus_addition_generator.py |
| `ACCEPT` | 2 | `ACCEPT\|(-5, -9)\|product 45 ✓, sum -14 ✓` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `AC_PRODUCT` | 2 | `AC_PRODUCT\|4 × (-3)\|-12` | factor_trinomial_generator.py |
| `ADD_COL` | 3 | `ADD_COL\|col_1\|0+0+0\|->0 (carry 0)` | multi_digit_addition_generator.py |
| `ADD_FORMULA` | 1 | `ADD_FORMULA\|P(A ∪ B) = P(A) + P(B)` | probability_addition_rule_generator.py |
| `ADD_PARTIALS` | 2 | `ADD_PARTIALS\|410370 + 3419750 + 61555500 + 68395000\|133780620` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `ADD_SETUP` | 2 | `ADD_SETUP\|P(A) = 2/12, P(B) = 4/12, mutually exclusive\|P(A ∪ B)` | probability_addition_rule_generator.py |
| `ALIGN_NUM` | 2 | `ALIGN_NUM\|817.63\|148.87` | number_comparison_generator.py |
| `AMPLITUDE` | 2 | `AMPLITUDE\|abs(5)\|5` | sinusoid_features_generator.py |
| `ANGLE_FORMULA` | 1 | `ANGLE_FORMULA\|add or subtract 360° until 0° ≤ θ < 360°` | angle_measure_generator.py |
| `ANGLE_RELATION` | 1 | `ANGLE_RELATION\|7x + 55 = 90` | angle_relationships_generator.py |
| `ANGLE_SETUP` | 2 | `ANGLE_SETUP\|complementary\|(2x + 15)° + (5x + 40)° = 90°` | angle_relationships_generator.py |
| `ANGLE_SOLVE` | 2 | `ANGLE_SOLVE\|7x = 35\|x = 5` | angle_relationships_generator.py |
| `ANTIDERIV` | 2 | `ANTIDERIV\|-16x^3\|-4x^4` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, definite_integral_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py |
| `APPROX_SETUP` | 2 | `APPROX_SETUP\|estimate √47\|linearize f(x) = √x at a = 49` | linear_approx_generator.py |
| `ARCLEN_FORMULA` | 1 | `ARCLEN_FORMULA\|L = ∫ √((dx/dt)^2 + (dy/dt)^2) dt` | arc_length_generator.py, parametric_calculus_generator.py |
| `ARC_FORMULA` | 1 | `ARC_FORMULA\|L = (θ/360)·2πr` | arc_sector_generator.py |
| `ARC_SETUP` | 2 | `ARC_SETUP\|circle r = 8, central angle 45°\|arc length` | arc_sector_generator.py |
| `AREA` | 1, 3 | `AREA\|80` | geometry_area_perimeter_generator.py |
| `AREA_SETUP` | 2 | `AREA_SETUP\|y = x^2 and y = 8x - 7\|area between the curves` | area_between_curves_generator.py |
| `ASYMPTOTE` | 1 | `ASYMPTOTE\|y = -1 ± (3/4)x` | hyperbola_features_generator.py |
| `B` | 1, 3 | `B\|38\|1\|381` | decimal_div_generator.py, long_division_generator.py, percent_problem_generator.py, polynomial_long_division_generator.py |
| `BASE_ADD_COL` | 3 | `BASE_ADD_COL\|col 0\|B + 1 + carry 0\|12 -> digit C, carry 0` | base_arithmetic_generator.py |
| `BASE_ARITH_SETUP` | 2 | `BASE_ARITH_SETUP\|base 16\|4FE * 9` | base_arithmetic_generator.py |
| `BASE_CARRY` | 2 | `BASE_CARRY\|carry 2\|digit 2, carry 0` | base_arithmetic_generator.py |
| `BASE_MUL_COL` | 3 | `BASE_MUL_COL\|col 0\|E * 9 + carry 0\|126 -> digit E, carry 7` | base_arithmetic_generator.py |
| `BASE_SETUP` | 2 | `BASE_SETUP\|11101101_2\|decimal` | base_conversion_generator.py |
| `BAYES_CELL` | 3 | `BAYES_CELL\|true positive\|60 * 7/10\|42` | conditional_probability_generator.py |
| `BAYES_FORMULA` | 1 | `BAYES_FORMULA\|P(disease=no given negative) = TN/(TN + FN)` | conditional_probability_generator.py |
| `BAYES_SETUP` | 3 | `BAYES_SETUP\|disease=yes 60, disease=no 72\|sensitivity 7/10, specificity 3/4\|P(disease=no given test negative)` | conditional_probability_generator.py |
| `BINOM_FORMULA` | 1 | `BINOM_FORMULA\|P(X ≤ k) = Σ C(n,i)·p^i·(1-p)^(n-i)` | binomial_probability_generator.py |
| `BINOM_SETUP` | 2 | `BINOM_SETUP\|n = 4, p = 1/5\|P(X ≤ 1)` | binomial_probability_generator.py |
| `BORROW` | 3 | `BORROW\|col_1\|from_left\|1` | multi_digit_subtraction_generator.py |
| `BRANCH_TEST` | 2 | `BRANCH_TEST\|3 <= 1\|no` | piecewise_evaluation_generator.py |
| `BRANCH_USE` | 1 | `BRANCH_USE\|$6.25` | piecewise_evaluation_generator.py |
| `BRING_DOWN` | 2 | `BRING_DOWN\|2\|current = 2` | composite_arithmetic_generator.py |
| `C` | 3 | `C\|3/2\|18\|27/18` | fraction_comparison_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `CALC` | 1 | `CALC\|x = -7` | systems_elimination_generator.py, systems_substitution_generator.py |
| `CANCEL` | 2 | `CANCEL\|(n - 8)\|(n + 3)/(n - 2)` | derivative_limit_def_generator.py, derivative_transcendental_generator.py, limit_evaluation_generator.py, power_series_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, series_convergence_generator.py, trig_identity_verify_generator.py |
| `CANDIDATES` | 1 | `CANDIDATES\|±1/2, ±1, ±2, ±4, ±8, ±16` | rational_root_generator.py |
| `CARRY_FINAL` | 1 | `CARRY_FINAL\|1` | multi_digit_addition_generator.py |
| `CBRT` | 2 | `CBRT\|64n^3\|4n` | factor_special_forms_generator.py, inverse_function_generator.py, rational_exponent_generator.py |
| `CEIL` | 2 | `CEIL\|51.380224\|52` | confidence_interval_generator.py |
| `CENTER` | 1 | `CENTER\|(2, -6)` | circle_equation_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py |
| `CHANGE_BASE` | 1 | `CHANGE_BASE\|log_9(81) = log_3(81)/log_3(9)` | log_conversion_generator.py |
| `CHECK` | 2, 3 | `CHECK\|multiply_back\|23×98+45=2299\|2299` | area_between_curves_generator.py, arithmetic_sequence_generator.py, base_arithmetic_generator.py, chi_square_generator.py, completing_square_generator.py, conditional_probability_generator.py, cramers_rule_generator.py, error_spotting_generator.py, expected_value_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, fill_in_step_generator.py, five_number_summary_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, horner_evaluation_generator.py, hypothesis_test_generator.py, inverse_function_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_fractional_generator.py, log_equation_generator.py, long_division_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, power_series_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_variable_simplify_generator.py, ratio_table_generator.py, recursive_explicit_generator.py, series_convergence_generator.py, similar_triangles_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, taylor_series_generator.py, tip_bill_split_generator.py, two_step_equation_generator.py, z_score_generator.py |
| `CHECK_POINT` | 3 | `CHECK_POINT\|x=0\|5·0 + 0 = 0\|5·0 + 0 = 0` | special_solution_equation_generator.py |
| `CHI_FORMULA` | 1 | `CHI_FORMULA\|E = (row·col)/N; χ² = Σ (O - E)^2/E` | chi_square_generator.py |
| `CHI_SETUP` | 2 | `CHI_SETUP\|row 1: 5, 15; row 2: 15, 65; N = 100\|independence; df = 1, critical value = 3.841` | chi_square_generator.py |
| `CHI_TERM` | 3 | `CHI_TERM\|5 - 4 = 1\|1^2 = 1\|1/4 = 0.25` | chi_square_generator.py |
| `CIRCLE_ANGLE_SETUP` | 2 | `CIRCLE_ANGLE_SETUP\|inscribed angle 44°\|central angle on the same arc` | circle_angle_generator.py |
| `CIRCLE_CALCULATE` | 2 | `CIRCLE_CALCULATE\|C = 18π\|18π` | circle_generator.py |
| `CIRCLE_FORMULA` | 1 | `CIRCLE_FORMULA\|C = πd` | circle_generator.py |
| `CIRCLE_SETUP` | 2 | `CIRCLE_SETUP\|18\|diameter` | circle_equation_generator.py, circle_generator.py |
| `CIRCLE_SUBSTITUTE` | 1 | `CIRCLE_SUBSTITUTE\|C = π × 18` | circle_generator.py |
| `CI_FORMULA` | 1 | `CI_FORMULA\|x̄ ± E` | confidence_interval_generator.py |
| `CI_SETUP` | 2 | `CI_SETUP\|σ = 27, n = 100, z* = 2.05\|margin of error` | confidence_interval_generator.py |
| `CMP` | 3 | `CMP\|9/3\|2/3\|>` | fraction_comparison_generator.py, graph_interpret_generator.py |
| `CMP_NUM` | 3 | `CMP_NUM\|817.63\|148.87\|>` | number_comparison_generator.py |
| `COEFFS` | 1, 2 | `COEFFS\|1, 1, -21, -1, 24` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `COFACTOR` | 2 | `COFACTOR\|(1,1) sign +\|minor [[4, 3], [-3, -4]]` | determinant_generator.py |
| `COMB_CONST` | 3 | `COMB_CONST\|-5\|+9\|4` | derivative_product_quotient_generator.py, equation_from_two_points_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMB_FORMULA` | 1 | `COMB_FORMULA\|C(n, r) = P(n, r)/r!` | permutation_combination_generator.py |
| `COMB_SETUP` | 2 | `COMB_SETUP\|choose 2 of 12\|order does not matter` | permutation_combination_generator.py |
| `COMB_X` | 3 | `COMB_X\|-2x\|-2x\|-4x` | derivative_product_quotient_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMMON_DIFF` | 2 | `COMMON_DIFF\|-7 - 0\|-7` | arithmetic_sequence_generator.py, recursive_explicit_generator.py |
| `COMMON_RATIO` | 2 | `COMMON_RATIO\|25/125\|1/5` | geometric_sequence_generator.py, recursive_explicit_generator.py |
| `COMPLETE_SQUARE` | 2 | `COMPLETE_SQUARE\|half of 2 = 1\|1^2 = 1` | completing_square_generator.py, conic_standard_form_generator.py, polar_parametric_generator.py |
| `COMPOSITE_FACTOR` | 2 | `COMPOSITE_FACTOR\|3\|47` | divisibility_classification_generator.py |
| `COMPOSITE_SETUP` | 2 | `COMPOSITE_SETUP\|area = length × width with mixed numbers\|convert, multiply, simplify` | composite_arithmetic_generator.py |
| `COMP_INEQ_PART` | 2 | `COMP_INEQ_PART\|Part 1\|x - 4 < -5 -> x < -1` | compound_inequality_generator.py |
| `COMP_INEQ_SETUP` | 1 | `COMP_INEQ_SETUP\|x - 4 < -5 OR x - 4 > 1` | compound_inequality_generator.py |
| `COND_COUNT` | 2 | `COND_COUNT\|club=no and commute=bike\|13` | conditional_probability_generator.py |
| `COND_FORMULA` | 1 | `COND_FORMULA\|P(A given B) = count(A and B)/count(B)` | conditional_probability_generator.py |
| `COND_SETUP` | 2 | `COND_SETUP\|yes/bike 13, no/bike 13, yes/bus 19, no/bus 11\|P(club=no given commute=bike)` | conditional_probability_generator.py |
| `COND_TOTAL` | 2 | `COND_TOTAL\|commute=bike total\|13 + 13 = 26` | conditional_probability_generator.py |
| `CONIC_SETUP` | 2 | `CONIC_SETUP\|(x + 2)^2 = -8(y - 4)\|vertex, focus, directrix` | conic_standard_form_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `CONJUGATE` | 2 | `CONJUGATE\|6 - 2i\|6 + 2i` | complex_division_generator.py |
| `CONVERGE_CHECK` | 2 | `CONVERGE_CHECK\|abs(r) = 1/5 < 1\|converges` | geometric_sequence_generator.py, series_convergence_generator.py |
| `CONV_FACTOR` | 2 | `CONV_FACTOR\|1 lb\|16 oz` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, unit_conversion_generator.py |
| `CONV_RESULT` | 2 | `CONV_RESULT\|2 lb\|32 oz` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, temperature_conversion_generator.py, unit_conversion_generator.py |
| `CORR_FORMULA` | 1 | `CORR_FORMULA\|r = Sxy/√(Sxx·Syy)` | regression_generator.py |
| `COUNT` | 2 | `COUNT\|A = [2, 4, 6]\|3/6` | probability_addition_rule_generator.py |
| `COUNT_DP` | 3 | `COUNT_DP\|2\|1\|3` | decimal_mult_generator.py |
| `CROSS_MULT` | 1 | `CROSS_MULT\|10·EF = 25·14` | similar_triangles_generator.py, triangle_solve_generator.py |
| `CURVE_SETUP` | 2 | `CURVE_SETUP\|f(x) = x^3 - 3x^2 - 9x + 7\|critical points and their nature` | curve_analysis_generator.py |
| `CX_SETUP` | 2 | `CX_SETUP\|(7 - 3i) + (1 + 8i)\|add` | complex_division_generator.py, complex_number_ops_generator.py |
| `D` | 3 | `D\|632\|99\|6` | antiderivative_generator.py, arithmetic_sequence_generator.py, circle_angle_generator.py, circle_equation_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, decimal_div_generator.py, definite_integral_generator.py, dimensional_analysis_generator.py, error_spotting_generator.py, exponential_equation_generator.py, exponential_model_generator.py, fill_in_step_generator.py, function_operations_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, hypothesis_test_generator.py, kinematics_generator.py, limit_evaluation_generator.py, linear_simple_generator.py, log_conversion_generator.py, logistic_growth_generator.py, long_division_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, nets_surface_area_generator.py, optimization_generator.py, order_of_operations_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, percent_problem_generator.py, permutation_combination_generator.py, physics_formula_generator.py, polar_parametric_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, regression_generator.py, regular_polygon_area_generator.py, riemann_sum_generator.py, right_triangle_trig_generator.py, round_solids_generator.py, segment_partition_generator.py, series_convergence_generator.py, similar_triangles_generator.py, simple_probability_generator.py, sinusoid_features_generator.py, slope_two_points_generator.py, special_right_triangle_generator.py, standard_deviation_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, u_substitution_generator.py, vector_ops_generator.py, z_score_generator.py |
| `DEC_ADD_COL` | 3 | `DEC_ADD_COL\|frac_0\|8+0+0\|->8 (carry 0)` | decimal_add_sub_generator.py |
| `DEC_ALIGN` | 2 | `DEC_ALIGN\|17.98\|23.20` | decimal_add_sub_generator.py |
| `DEC_CARRY_FINAL` | 1 | `DEC_CARRY_FINAL\|1` | decimal_add_sub_generator.py |
| `DEC_SHIFT` | 3 | `DEC_SHIFT\|7.5/1.0\|7.5/10\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `DEC_SUB_COL` | 3 | `DEC_SUB_COL\|frac_0\|7-1 (borrow_in 0)\|->6 (borrow_out 0)` | decimal_add_sub_generator.py |
| `DEC_TO_FRAC` | 2 | `DEC_TO_FRAC\|0.1\|1/10` | fraction_decimal_percent_converter.py |
| `DEC_TO_PERCENT` | 2 | `DEC_TO_PERCENT\|1\|100.00%` | fraction_decimal_percent_converter.py, percent_problem_generator.py, tip_bill_split_generator.py |
| `DEC_TYPE` | 2 | `DEC_TYPE\|7/10\|terminating` | repeating_decimal_generator.py |
| `DEC_VALUE` | 2 | `DEC_VALUE\|7/10\|0.7` | repeating_decimal_generator.py |
| `DEGREE_COMPARE` | 2 | `DEGREE_COMPARE\|deg num = deg den = 2\|y = 1/1` | limit_evaluation_generator.py, rational_function_features_generator.py, series_convergence_generator.py |
| `DERIV_RULE` | 2 | `DERIV_RULE\|power rule\|d/dx of c·x^n = c·n·x^(n-1)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py |
| `DERIV_SETUP` | 2 | `DERIV_SETUP\|f(x) = x^3 - 3x + 4x^(-1)\|f'(x)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, log_diff_higher_order_generator.py, tangent_line_generator.py |
| `DET_FORMULA` | 1 | `DET_FORMULA\|det = a11·M11 - a12·M12 + a13·M13` | cramers_rule_generator.py, determinant_generator.py, matrix_inverse_generator.py |
| `DEV_ROW` | 3 | `DEV_ROW\|23\|-3\|9` | standard_deviation_generator.py |
| `DIRECTRIX` | 1 | `DIRECTRIX\|y = 6` | parabola_features_generator.py |
| `DISC` | 2, 3 | `DISC\|9\|-40\|49` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `DISC_CLASSIFY` | 2 | `DISC_CLASSIFY\|-28 < 0\|no real solutions` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py |
| `DIST` | 3 | `DIST\|3\|3x-4\|9x-12` | derivative_limit_def_generator.py, derivative_product_quotient_generator.py, equation_from_two_points_generator.py, function_composition_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, polar_parametric_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, simplify_expression_generator.py, solid_revolution_generator.py, special_solution_equation_generator.py, tangent_line_generator.py |
| `DIST_COMBINE` | 1 | `DIST_COMBINE\|-18y + -65 = 25` | systems_substitution_generator.py |
| `DIST_FORMULA` | 1 | `DIST_FORMULA\|d = √((x2 - x1)^2 + (y2 - y1)^2)` | distance_formula_generator.py, hypercube_counting_generator.py |
| `DIST_TERM` | 2 | `DIST_TERM\|2x\|6x^3 - 2x^2 + 6x` | multiplying_polynomials_generator.py |
| `DIVMOD` | 4 | `DIVMOD\|149\|2\|74\|r=1` | base_conversion_generator.py |
| `DIV_CHECK` | 3 | `DIV_CHECK\|89\|2\|1` | divisibility_classification_generator.py |
| `DIV_COEFF` | 3 | `DIV_COEFF\|4\|-4\|x=-1` | linear_complex_generator.py |
| `DIV_SETUP` | 2 | `DIV_SETUP\|75\|10` | decimal_div_generator.py, percent_problem_generator.py |
| `DIV_TERM` | 3 | `DIV_TERM\|15t^6\|3t^2\|5t^4` | factor_gcf_generator.py, polynomial_long_division_generator.py |
| `DOMAIN_COND` | 2 | `DOMAIN_COND\|radicand ≥ 0\|t + 6 ≥ 0` | domain_range_generator.py |
| `DOMAIN_NOTE` | 2 | `DOMAIN_NOTE\|x ≠ 9\|denominator cannot be zero` | domain_range_generator.py, log_equation_generator.py, logistic_growth_generator.py, probability_addition_rule_generator.py, rational_equation_generator.py, unit_circle_generator.py |
| `DOT_FORMULA` | 1 | `DOT_FORMULA\|cos θ = (u·v)/(‖u‖ · ‖v‖)` | dot_product_generator.py |
| `E` | 3 | `E\|14\|2\|196` | arc_sector_generator.py, circle_equation_generator.py, complex_division_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, distance_formula_generator.py, ellipse_features_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, finance_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, hyperbola_features_generator.py, hypercube_counting_generator.py, limit_evaluation_generator.py, log_conversion_generator.py, log_equation_generator.py, log_properties_generator.py, mean_value_theorem_generator.py, optimization_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, pythag_hyp_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, round_solids_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py |
| `EQUATE_EXP` | 1 | `EQUATE_EXP\|5x = 3` | exponential_equation_generator.py |
| `EQ_2PT_SETUP` | 2 | `EQ_2PT_SETUP\|(-4, 7)\|(-2, 2)` | equation_from_two_points_generator.py |
| `EQ_OP_BOTH` | 4 | `EQ_OP_BOTH\|subtract\|1\|x\|6` | absolute_value_equation_generator.py, area_between_curves_generator.py, completing_square_generator.py, curve_analysis_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, implicit_diff_generator.py, inverse_function_generator.py, linear_fractional_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, mean_value_theorem_generator.py, one_step_equation_generator.py, optimization_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, separable_ode_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_OP_NOTE` | 3 | `EQ_OP_NOTE\|subtract\|b\|from both sides` | equation_from_two_points_generator.py, literal_equation_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `EQ_RESULT` | 2 | `EQ_RESULT\|x\|6` | completing_square_generator.py, error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, one_step_equation_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, special_solution_equation_generator.py, two_step_equation_generator.py |
| `EQ_SETUP` | 1, 2 | `EQ_SETUP\|x = 36/2` | area_between_curves_generator.py, completing_square_generator.py, complex_quadratic_generator.py, cramers_rule_generator.py, discriminant_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_equation_generator.py, one_step_equation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, remainder_factor_theorem_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_SIMPLIFY` | 1 | `EQ_SIMPLIFY\|2x = -6` | error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, two_step_equation_generator.py |
| `ESTIMATE` | 2 | `ESTIMATE\|95422 × 54058 ≈ 100000 × 50000\|5000000000` | long_division_generator.py, multi_digit_multiplication_generator.py |
| `ESTIMATE_CHECK` | 3 | `ESTIMATE_CHECK\|5000000000\|5158322476\|5158322476 ≈ 5000000000 ✓` | long_division_generator.py, multi_digit_multiplication_generator.py |
| `EULER_FORMULA` | 1 | `EULER_FORMULA\|χ = V - E + F` | euler_characteristic_generator.py |
| `EULER_NOTE` | 2 | `EULER_NOTE\|2\|sphere-family polyhedron: χ is always 2` | euler_characteristic_generator.py |
| `EULER_SETUP` | 2 | `EULER_SETUP\|hexagonal prism: V = 12, E = 18, F = 8\|V - E + F` | euler_characteristic_generator.py |
| `EVAL` | 1, 2 | `EVAL\|f(-4)\|24` | arc_length_generator.py, area_between_curves_generator.py, circle_equation_generator.py, complex_division_generator.py, composite_arithmetic_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dot_product_generator.py, ellipse_features_generator.py, euler_method_generator.py, five_number_summary_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, improper_integral_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_properties_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, power_series_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, row_reduction_generator.py, solid_revolution_generator.py, standard_deviation_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py |
| `EV_FORMULA` | 1 | `EV_FORMULA\|E[X] = Σ x·P(x)` | expected_value_generator.py |
| `EV_SETUP` | 2 | `EV_SETUP\|P(X=2) = 1/5; P(X=9) = 1/10; P(X=3) = 3/5; P(X=1) = 1/10\|E[X]` | expected_value_generator.py |
| `EXP_CELL` | 2 | `EXP_CELL\|(20·20)/100\|4` | chi_square_generator.py |
| `EXP_EXPAND` | 1 | `EXP_EXPAND\|(-3) × (-3) × (-3)` | exponent_generator.py |
| `EXP_PARTIAL` | 3 | `EXP_PARTIAL\|-3\|-3\|9` | exponent_generator.py |
| `EXP_RULE_APPLY` | 4 | `EXP_RULE_APPLY\|add\|5\|4\|9` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_RULE_IDENTIFY` | 2 | `EXP_RULE_IDENTIFY\|zero_exponent\|x^0 = 1 (for x ≠ 0)` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SETUP` | 1 | `EXP_RULE_SETUP\|(2x)^0` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SIMPLIFY` | 1 | `EXP_RULE_SIMPLIFY\|1` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_SETUP` | 2 | `EXP_SETUP\|-3\|3` | exponent_generator.py |
| `F` | 2 | `F\|9/9\|1` | composite_arithmetic_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, repeating_decimal_generator.py, simple_probability_generator.py, slope_two_points_generator.py |
| `FACTOR_GROUP` | 3 | `FACTOR_GROUP\|4x^2 - x\|x\|(4x - 1)` | conic_standard_form_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, factor_grouping_generator.py, factor_trinomial_generator.py |
| `FACTOR_PAIR_GOAL` | 2 | `FACTOR_PAIR_GOAL\|m·n = 45\|m + n = -14` | factor_trinomial_generator.py |
| `FACT_CHECK` | 3 | `FACT_CHECK\|107\|1\|0` | factors_generator.py |
| `FACT_FORMULA` | 1 | `FACT_FORMULA\|5! = 1·2·3·4·5` | permutation_combination_generator.py |
| `FACT_PAIR` | 2 | `FACT_PAIR\|1\|107` | factors_generator.py |
| `FACT_SETUP` | 2 | `FACT_SETUP\|5!\|expand the factorial` | permutation_combination_generator.py |
| `FIND_SLOPE` | 2 | `FIND_SLOPE\|Given slope (m1)\|-3` | parallel_perpendicular_line_generator.py |
| `FIN_FORMULA` | 1 | `FIN_FORMULA\|I = P*r*t; A = P + I` | finance_generator.py |
| `FIN_SETUP` | 3 | `FIN_SETUP\|simple interest P = 500\|r = 8%, t = 4\|interest and balance` | finance_generator.py |
| `FLAG` | 2 | `FLAG\|4\|7 × 8 = 56, not 72` | error_spotting_generator.py |
| `FOCUS` | 1 | `FOCUS\|(-2, 2)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `FOIL_F` | 2 | `FOIL_F\|First: 4 * (-5)\|-20` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_I` | 2 | `FOIL_I\|Inner: 7i * (-5)\|-35i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_L` | 2 | `FOIL_L\|Last: 7i * 7i\|49i^2` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_O` | 2 | `FOIL_O\|Outer: 4 * 7i\|28i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_SETUP` | 1 | `FOIL_SETUP\|(4 + √2)(2 + √2)` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py, radical_multiply_generator.py, trig_identity_verify_generator.py |
| `FORM_IDENTIFY` | 2 | `FORM_IDENTIFY\|difference_of_squares\|a^2 - b^2 = (a - b)(a + b)` | completing_square_generator.py, conic_standard_form_generator.py, ellipse_features_generator.py, factor_special_forms_generator.py, hyperbola_features_generator.py, parabola_features_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py |
| `FRAC_BUILD` | 2 | `FRAC_BUILD\|56/300\|14/75` | conditional_probability_generator.py, geometric_probability_generator.py |
| `FRAC_REDUCE` | 2 | `FRAC_REDUCE\|24/-16\|-3/2` | angle_measure_generator.py, arc_length_generator.py, arc_sector_generator.py, complex_division_generator.py, frequency_table_generator.py, function_operations_generator.py, hyperbola_features_generator.py, implicit_diff_generator.py, improper_integral_generator.py, probability_addition_rule_generator.py, related_rates_generator.py, right_triangle_trig_generator.py |
| `FRAC_TO_DEC` | 2 | `FRAC_TO_DEC\|2/6\|0.3333333333` | fraction_decimal_percent_converter.py |
| `FREQ_SETUP` | 2 | `FREQ_SETUP\|table — Apple: 5, Banana: 10, Cherry: 4, Grape: 5\|most frequent category` | frequency_table_generator.py |
| `FUNC_OP` | 2 | `FUNC_OP\|(f/g)(-4)\|f(-4)/g(-4)` | function_composition_generator.py, function_operations_generator.py |
| `FUNC_SETUP` | 2 | `FUNC_SETUP\|x: -4, -3, -2, -1, 4; f(x): -11, 26, -8, -6, 13\|f(-3)` | domain_range_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, inverse_function_generator.py, piecewise_evaluation_generator.py, rational_function_features_generator.py |
| `GCD_RESULT` | 1 | `GCD_RESULT\|2` | lcm_generator.py |
| `GCD_START` | 2 | `GCD_START\|35\|61` | gcf_generator.py, lcm_generator.py |
| `GCD_STEP` | 3 | `GCD_STEP\|35\|61\|35` | gcf_generator.py, lcm_generator.py |
| `GCF_COEFF` | 2 | `GCF_COEFF\|15, 24, 9\|3` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_RESULT` | 1 | `GCF_RESULT\|3t^2` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_VAR` | 2 | `GCF_VAR\|t^6, t^3, t^2\|t^2` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GEOM_FORMULA` | 1 | `GEOM_FORMULA\|P(X > k) = (1-p)^k` | geometric_distribution_generator.py |
| `GEOM_SETUP` | 2 | `GEOM_SETUP\|p = 1/3, q = 2/3\|P(X > 6)` | geometric_distribution_generator.py |
| `GEO_PROB_FORMULA` | 1 | `GEO_PROB_FORMULA\|probability = favorable area / total area` | geometric_probability_generator.py |
| `GEO_PROB_SETUP` | 2 | `GEO_PROB_SETUP\|rectangle 20 by 15\|shaded rectangle 14 by 4` | geometric_probability_generator.py |
| `GEO_SETUP` | 2 | `GEO_SETUP\|right triangle, altitude h = 10 to the hypotenuse; one segment p = 4\|the other segment q` | geometric_mean_generator.py |
| `GOAL` | 1 | `GOAL\|Convert to Slope-Intercept Form (y = mx + b)` | point_slope_generator.py, standard_form_conversion_generator.py |
| `GRAPH_CHANGE` | 3 | `GRAPH_CHANGE\|Jan\|Feb\|0` | graph_interpret_generator.py |
| `GRAPH_DATA` | 2 | `GRAPH_DATA\|bar_chart\|English:44,Music:8,Art:26,Math:22,History:45,Science:12` | graph_interpret_generator.py |
| `GRAPH_MAX` | 2 | `GRAPH_MAX\|2019\|28` | graph_interpret_generator.py |
| `GRAPH_MAX_CHANGE` | 3 | `GRAPH_MAX_CHANGE\|Feb\|Mar\|2` | graph_interpret_generator.py |
| `GRAPH_MIN` | 2 | `GRAPH_MIN\|Week 2\|23` | graph_interpret_generator.py |
| `GRAPH_READ` | 2 | `GRAPH_READ\|Science\|12` | graph_interpret_generator.py |
| `GROUP` | 2 | `GROUP\|(4x^2 - x)\|(12x - 3)` | factor_grouping_generator.py, factor_trinomial_generator.py |
| `HA` | 1 | `HA\|y = 1` | rational_function_features_generator.py |
| `HOLE` | 1 | `HOLE\|x = 3` | rational_function_features_generator.py |
| `HORNER_SETUP` | 2 | `HORNER_SETUP\|-x^3 - x^2 - 2x - 5\|x = -1` | horner_evaluation_generator.py |
| `HT_SETUP` | 2 | `HT_SETUP\|H0: p = 0.5; Ha: p ≠ 0.5\|n = 25, 8 successes, critical value = 1.645` | hypothesis_test_generator.py |
| `HYPERCUBE_FORMULA` | 1 | `HYPERCUBE_FORMULA\|diagonal = s·√n` | hypercube_counting_generator.py |
| `HYPERCUBE_SETUP` | 2 | `HYPERCUBE_SETUP\|points P(-2, -5, -5, 0) and Q(2, -2, -3, -4) in R^4\|distance` | hypercube_counting_generator.py |
| `I` | 2 | `I\|3/2\|2/3` | fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_mult_div_generator.py |
| `IDENTIFY` | 2 | `IDENTIFY\|order matters\|use P(n, r)` | permutation_combination_generator.py |
| `IDENTITY_SETUP` | 2 | `IDENTITY_SETUP\|verify: cos x · cot x = csc x - sin x\|transform the right side` | trig_identity_verify_generator.py |
| `IDENT_MATCH` | 1 | `IDENT_MATCH\|cos x · cot x = cos x · cot x` | trig_identity_verify_generator.py |
| `IDENT_SUB` | 1 | `IDENT_SUB\|csc x = 1/sin x` | parametric_calculus_generator.py, trig_identity_verify_generator.py |
| `IMPLICIT_DIFF` | 2 | `IMPLICIT_DIFF\|d/dx of x^3\|3x^2` | implicit_diff_generator.py, log_diff_higher_order_generator.py, related_rates_generator.py |
| `IMPLICIT_SETUP` | 2 | `IMPLICIT_SETUP\|x^3 + y^3 = 65\|dy/dx` | implicit_diff_generator.py |
| `IMPROPER_TO_MIX` | 2 | `IMPROPER_TO_MIX\|75/14\|5 5/14` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `INEQ_FLIP` | 1 | `INEQ_FLIP\|Dividing by negative number reverses inequality` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_OP_ALL` | 3 | `INEQ_OP_ALL\|subtract\|10\|-26 < 2x < 6` | absolute_value_inequality_generator.py, compound_inequality_generator.py |
| `INEQ_OP_BOTH` | 4 | `INEQ_OP_BOTH\|multiply\|7\|x\|7` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_RESULT` | 3 | `INEQ_RESULT\|x\|≥\|7` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SETUP` | 1 | `INEQ_SETUP\|x/7 ≥ 1` | linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SIMPLIFY` | 1 | `INEQ_SIMPLIFY\|x/3 > 5` | domain_range_generator.py, two_step_inequality_generator.py |
| `INTEG_RULE` | 2 | `INTEG_RULE\|power rule\|∫ x^n dx = x^(n+1)/(n+1) + C` | antiderivative_generator.py, definite_integral_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py |
| `INTEG_SETUP` | 2 | `INTEG_SETUP\|∫ (-16x^3 + 6x^2) dx\|antiderivative` | antiderivative_generator.py, arc_length_generator.py, definite_integral_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, u_substitution_generator.py |
| `INTERCEPT_FORMULA` | 1 | `INTERCEPT_FORMULA\|a = ȳ - b·x̄` | regression_generator.py |
| `INT_ABS` | 2 | `INT_ABS\|-14\|14` | integer_operations_generator.py |
| `INT_ALIGN` | 2 | `INT_ALIGN\|82320\|65750` | multi_digit_addition_generator.py, multi_digit_subtraction_generator.py |
| `INT_APPLY_SIGN` | 3 | `INT_APPLY_SIGN\|24\|negative\|-24` | integer_operations_generator.py |
| `INT_OP` | 4 | `INT_OP\|-\|14\|14\|0` | integer_operations_generator.py |
| `INT_REWRITE` | 2 | `INT_REWRITE\|-14 - (-14)\|-14 + 14` | integer_operations_generator.py |
| `INT_SIGN_RULE` | 2 | `INT_SIGN_RULE\|subtract_rule\|Subtracting is adding the opposite` | integer_operations_generator.py |
| `INV_FORMULA` | 1 | `INV_FORMULA\|A⁻¹ = (1/det)·[[d, -b], [-c, a]]` | matrix_inverse_generator.py |
| `IVT_SETUP` | 2 | `IVT_SETUP\|f(x) = x^3 + 3x - 8 on [-1, 0]\|does the IVT guarantee a root?` | mean_value_theorem_generator.py |
| `I_CYCLE` | 2 | `I_CYCLE\|i^0\|1` | complex_number_ops_generator.py |
| `I_SQUARE` | 2 | `I_SQUARE\|49i^2\|-49` | complex_division_generator.py, complex_number_ops_generator.py |
| `KIN_FORMULA` | 1 | `KIN_FORMULA\|d = v*t` | kinematics_generator.py |
| `KIN_SETUP` | 3 | `KIN_SETUP\|v = 77 ft/s\|t = 4 seconds\|distance` | kinematics_generator.py |
| `L` | 3 | `L\|2\|9\|18` | fraction_comparison_generator.py, fraction_op_generator.py, linear_fractional_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `LCM_FROM_GCD` | 3 | `LCM_FROM_GCD\|54*50\|2\|1350` | lcm_generator.py |
| `LIMIT_SETUP` | 1, 2 | `LIMIT_SETUP\|lim x→0 of (√(x + 25) - 5)/x\|0/0: rationalize` | derivative_limit_def_generator.py, improper_integral_generator.py, lhopital_generator.py, limit_evaluation_generator.py, power_series_generator.py, series_convergence_generator.py |
| `LINE_RELATION_SETUP` | 3 | `LINE_RELATION_SETUP\|parallel\|y = -3x - 2\|(2, -10)` | parallel_perpendicular_line_generator.py |
| `LOG_BOTH_SIDES` | 1 | `LOG_BOTH_SIDES\|log_5(5^x) = log_5(17)` | exponential_equation_generator.py, log_diff_higher_order_generator.py, separable_ode_generator.py |
| `LOG_FORM` | 1 | `LOG_FORM\|b^y = x ⟺ log_b(x) = y` | log_conversion_generator.py, log_equation_generator.py |
| `LOG_IDENT` | 2 | `LOG_IDENT\|ln(e) = 1\|1` | exponential_equation_generator.py, log_conversion_generator.py |
| `LOG_ONE_TO_ONE` | 1 | `LOG_ONE_TO_ONE\|4x + 8 = x - 7` | log_equation_generator.py |
| `LOG_POWER` | 2 | `LOG_POWER\|log_3(y^2)\|2log_3(y)` | log_diff_higher_order_generator.py, log_properties_generator.py |
| `LOG_PRODUCT` | 2 | `LOG_PRODUCT\|log_3(xy^2)\|log_3(x) + log_3(y^2)` | log_equation_generator.py, log_properties_generator.py |
| `LOG_QUOTIENT` | 2 | `LOG_QUOTIENT\|log_2(x/y)\|log_2(x) - log_2(y)` | log_properties_generator.py |
| `LOG_SETUP` | 2 | `LOG_SETUP\|log_3(xy^2)\|expand` | log_properties_generator.py |
| `M` | 2, 3 | `M\|6\|99\|594` | angle_measure_generator.py, arc_length_generator.py, arc_sector_generator.py, arithmetic_sequence_generator.py, binomial_probability_generator.py, chain_rule_generator.py, circle_angle_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, decimal_div_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dimensional_analysis_generator.py, dot_product_generator.py, error_spotting_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, fill_in_step_generator.py, finance_generator.py, five_number_summary_generator.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, horner_evaluation_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, kinematics_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, long_division_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, multi_step_unit_conversion_generator.py, nets_surface_area_generator.py, optimization_generator.py, order_of_operations_generator.py, parametric_calculus_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, permutation_combination_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, recursive_explicit_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, right_triangle_trig_generator.py, round_solids_generator.py, row_reduction_generator.py, segment_partition_generator.py, similar_triangles_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, unit_circle_generator.py, unit_conversion_generator.py, vector_ops_generator.py, volume_rect_prism_generator.py, z_score_generator.py |
| `MAG_FORMULA` | 1 | `MAG_FORMULA\|magnitude = √(x^2 + y^2)` | vector_ops_generator.py |
| `MAT_ENTRY` | 2 | `MAT_ENTRY\|(1,1)\|-15` | matrix_ops_generator.py |
| `MAT_SETUP` | 2 | `MAT_SETUP\|A = [[-3, -5], [-2, 0]]\|5A` | determinant_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, row_reduction_generator.py |
| `MAX` | 2 | `MAX\|5, 6\|6` | taxicab_geometry_generator.py |
| `MEAN_DIV` | 3 | `MEAN_DIV\|71\|7\|10.142857142857142` | composite_arithmetic_generator.py, five_number_summary_generator.py, regression_generator.py, simple_stats_generator.py, standard_deviation_generator.py |
| `MEASURE_FAVORABLE` | 2 | `MEASURE_FAVORABLE\|shaded area\|14 * 4 = 56` | geometric_probability_generator.py |
| `MEASURE_TOTAL` | 2 | `MEASURE_TOTAL\|whole area\|20 * 15 = 300` | geometric_probability_generator.py |
| `MEDIAN_PAIR` | 2 | `MEDIAN_PAIR\|9\|12` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEDIAN_PICK` | 2, 3 | `MEDIAN_PICK\|16\|\|16` | five_number_summary_generator.py, simple_stats_generator.py |
| `METRIC` | 2 | `METRIC\|taxicab circle\|all points with abs(x) + abs(y) = 9` | taxicab_geometry_generator.py |
| `MIDLINE` | 1 | `MIDLINE\|y = 5` | sinusoid_features_generator.py |
| `MID_FORMULA` | 1 | `MID_FORMULA\|M = ((x1 + x2)/2, (y1 + y2)/2)` | circle_equation_generator.py, midpoint_generator.py |
| `MIX_IMPROPER` | 2 | `MIX_IMPROPER\|5 9/10\|59/10` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `MODE` | 2 | `MODE\|2\|1` | frequency_table_generator.py, simple_stats_generator.py |
| `MODEL` | 1 | `MODEL\|A = P(1 + r)^t` | exponential_model_generator.py |
| `MODEL_APPLY` | 1 | `MODEL_APPLY\|A = 2000 · (1 + 0.5)^2` | exponential_model_generator.py |
| `MODE_COUNT` | 2 | `MODE_COUNT\|1\|1` | simple_stats_generator.py |
| `MOE_FORMULA` | 1 | `MOE_FORMULA\|E = z*·σ/√n` | confidence_interval_generator.py |
| `MONO_ADD_EXP` | 2 | `MONO_ADD_EXP\|x^7 * x^2 = x^(7+2)\|x^9` | monomial_mult_div_generator.py |
| `MONO_DIV_COEFF` | 2 | `MONO_DIV_COEFF\|45 / 9\|5` | monomial_mult_div_generator.py |
| `MONO_MULT_COEFF` | 2 | `MONO_MULT_COEFF\|-8 * -2\|16` | monomial_mult_div_generator.py |
| `MONO_SETUP` | 1 | `MONO_SETUP\|(45x^6) / (9x^5)` | monomial_mult_div_generator.py |
| `MONO_SUB_EXP` | 2 | `MONO_SUB_EXP\|x^6 / x^5 = x^(6-5)\|x^1 = x` | monomial_mult_div_generator.py |
| `MOVE_TERM` | 2, 3 | `MOVE_TERM\|+2x\|left\|-2x-9-2x = -5` | area_between_curves_generator.py, completing_square_generator.py, conic_standard_form_generator.py, linear_complex_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py |
| `MUL_PARTIAL` | 3 | `MUL_PARTIAL\|6\|68395\|410370` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_SETUP` | 2 | `MUL_SETUP\|68395\|1956` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_TERM` | 3 | `MUL_TERM\|10\|-8.2x\|-82x` | linear_fractional_generator.py, polynomial_long_division_generator.py, rational_equation_generator.py |
| `MVT_SETUP` | 2 | `MVT_SETUP\|f(x) = x^2 + 5x - 3 on [-4, 4]\|find the c guaranteed by the MVT` | mean_value_theorem_generator.py |
| `NCR` | 2 | `NCR\|C(4,1)\|4` | binomial_probability_generator.py, hypercube_counting_generator.py |
| `NEED` | 2 | `NEED\|line 2 gives the base ratio 11:6\|line 4 multiplies 11 by 3` | fill_in_step_generator.py |
| `NET_SETUP` | 2 | `NET_SETUP\|6 squares 6 by 6\|total surface area` | nets_surface_area_generator.py |
| `NEW_SLOPE` | 2 | `NEW_SLOPE\|New slope (m2) = -3\|Parallel lines have the same slope` | parallel_perpendicular_line_generator.py |
| `NORMAL_SLOPE` | 2 | `NORMAL_SLOPE\|-1/(11)\|-1/11` | tangent_line_generator.py |
| `NORM_SETUP` | 2 | `NORM_SETUP\|X ~ N(57, 2)\|z-score of x = 60` | normal_table_generator.py, z_score_generator.py |
| `ODE_SETUP` | 2 | `ODE_SETUP\|dy/dt = ky; y doubles every 3 hours\|find k exactly` | euler_method_generator.py, logistic_growth_generator.py, separable_ode_generator.py |
| `OPT_SETUP` | 2 | `OPT_SETUP\|64 m of fence, barn forms the fourth side; sides x, x, and 64 - 2x\|maximize area` | optimization_generator.py |
| `PARALLEL_RELATION` | 1 | `PARALLEL_RELATION\|2x + 26 = 6x - 38` | angle_relationships_generator.py |
| `PARALLEL_SETUP` | 2 | `PARALLEL_SETUP\|alternate_interior\|Alternate interior angles are equal` | angle_relationships_generator.py |
| `PARALLEL_SOLVE` | 2 | `PARALLEL_SOLVE\|-4x = -64\|x = 16` | angle_relationships_generator.py |
| `PARAM_SETUP` | 2 | `PARAM_SETUP\|x = 3 cos t, y = 3 sin t\|eliminate t` | parametric_calculus_generator.py, polar_parametric_generator.py |
| `PARTFRAC_SETUP` | 1 | `PARTFRAC_SETUP\|(3x - 6)/((x - 1)(x - 4)) = A/(x - 1) + B/(x - 4)` | partial_fractions_generator.py |
| `PARTS_CHOOSE` | 2 | `PARTS_CHOOSE\|u = x, dv = e^x dx\|du = 1 dx, v = e^x` | integration_by_parts_generator.py |
| `PARTS_FORMULA` | 1 | `PARTS_FORMULA\|∫ u dv = uv - ∫ v du` | integration_by_parts_generator.py |
| `PASCAL_ROW` | 2 | `PASCAL_ROW\|0\|1` | pascal_triangle_generator.py |
| `PASCAL_SETUP` | 1 | `PASCAL_SETUP\|row 10` | pascal_triangle_generator.py |
| `PERCENT_CALC_PART` | 3 | `PERCENT_CALC_PART\|0.6\|150\|90` | percent_problem_generator.py |
| `PERCENT_TO_DEC` | 2 | `PERCENT_TO_DEC\|90%\|0.9` | composite_arithmetic_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finance_generator.py, fraction_decimal_percent_converter.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, tip_bill_split_generator.py |
| `PERIM` | 1 | `PERIM\|32` | geometry_area_perimeter_generator.py, polygon_perimeter_generator.py |
| `PERIOD` | 1 | `PERIOD\|π` | sinusoid_features_generator.py |
| `PERM_FORMULA` | 1 | `PERM_FORMULA\|P(n, r) = n·(n-1)···(n-r+1), 3 factors` | permutation_combination_generator.py |
| `PERM_SETUP` | 2 | `PERM_SETUP\|P(11, 3)\|n!/(n-r)!` | permutation_combination_generator.py |
| `PF_PRIME` | 1 | `PF_PRIME\|17` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PF_STEP` | 3 | `PF_STEP\|102\|2\|51` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PHASE_SHIFT` | 1 | `PHASE_SHIFT\|π/4 right` | sinusoid_features_generator.py |
| `PHYS_FORMULA` | 1 | `PHYS_FORMULA\|P = W/t` | physics_formula_generator.py |
| `PHYS_SETUP` | 3 | `PHYS_SETUP\|W = 1314 joules\|t = 9 seconds\|power` | physics_formula_generator.py |
| `PICTO_COUNT` | 2 | `PICTO_COUNT\|Cars\|8` | graph_interpret_generator.py |
| `PICTO_KEY` | 2 | `PICTO_KEY\|♦\|5` | graph_interpret_generator.py |
| `PLACE_DP` | 3 | `PLACE_DP\|4060686\|3\|4060.686` | decimal_mult_generator.py |
| `PLACE_DP_Q` | 2 | `PLACE_DP_Q\|75\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `PLACE_VALUE` | 2 | `PLACE_VALUE\|1 * 2^0\|1` | base_conversion_generator.py |
| `PLUS_MINUS` | 2 | `PLUS_MINUS\|x = ±4\|x = 4 or x = -4` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `POINT_SLOPE_SETUP` | 1 | `POINT_SLOPE_SETUP\|y - 7 = -5/2(x + 4)` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py |
| `POLAR_AREA_FORMULA` | 1 | `POLAR_AREA_FORMULA\|A = (1/2) ∫ r^2 dθ` | parametric_calculus_generator.py |
| `POLAR_FORMULA` | 1 | `POLAR_FORMULA\|x = r cos θ, y = r sin θ` | polar_parametric_generator.py |
| `POLAR_SETUP` | 2 | `POLAR_SETUP\|(r, θ) = (6, 240°)\|rectangular coordinates` | parametric_calculus_generator.py, polar_parametric_generator.py |
| `POLYDIV_SETUP` | 2 | `POLYDIV_SETUP\|6x^3 - 8x^2 - 7x - 6\|3x - 1` | polynomial_long_division_generator.py |
| `POLY_COMBINE` | 1 | `POLY_COMBINE\|2x^3 - x^2 - 2` | multiplying_binomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_DIST_NEG` | 1 | `POLY_DIST_NEG\|Distribute negative sign to second polynomial` | polynomial_add_sub_generator.py |
| `POLY_DIV_SETUP` | 1 | `POLY_DIV_SETUP\|(21x^5 - 35x^4 - 7x^2 + 7x^2) / (7x^2)` | polynomial_div_monomial_generator.py |
| `POLY_DIV_SPLIT` | 1 | `POLY_DIV_SPLIT\|(21x^5) / (7x^2) + (-35x^4) / (7x^2) + (-7x^2) / (7x^2) + (7x^2) / (7x^2)` | polynomial_div_monomial_generator.py |
| `POLY_FORMULA` | 1 | `POLY_FORMULA\|A = (1/2)·a·P` | regular_polygon_area_generator.py |
| `POLY_GROUP_LIKE` | 1 | `POLY_GROUP_LIKE\|(2x^3) + (-1x^2) + (-3x +3x) + (-8 +6)` | multiplying_polynomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_MULT_SETUP` | 1 | `POLY_MULT_SETUP\|(2x - 3)(3x^2 - x + 3)` | multiplying_polynomials_generator.py |
| `POLY_SETUP` | 1, 2 | `POLY_SETUP\|(-3x - 8) - (-2x^3 + x^2 - 3x - 6)` | factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, polynomial_add_sub_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, regular_polygon_area_generator.py |
| `POLY_SUB` | 2 | `POLY_SUB\|(6x^3 - 8x^2) - (6x^3 - 2x^2)\|-6x^2` | polynomial_long_division_generator.py |
| `POW` | 2 | `POW\|(1/5)^1\|0.2` | binomial_probability_generator.py, geometric_distribution_generator.py |
| `POWER_RULE` | 2 | `POWER_RULE\|x^3\|3x^2` | chain_rule_generator.py, curve_analysis_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, mean_value_theorem_generator.py, optimization_generator.py, tangent_line_generator.py |
| `PRIME` | 1 | `PRIME\|89` | divisibility_classification_generator.py |
| `PROB_CONDITIONAL` | 2 | `PROB_CONDITIONAL\|P(blue\|first was red)\|3/5` | compound_probability_generator.py |
| `PROB_DEPENDENT` | 1 | `PROB_DEPENDENT\|Drawing without replacement means dependent events` | compound_probability_generator.py |
| `PROB_DESCRIBE` | 1 | `PROB_DESCRIBE\|Coin flip and die roll, looking for tails and 1` | compound_probability_generator.py |
| `PROB_IDENTIFY` | 2 | `PROB_IDENTIFY\|P(tails)\|1/2` | compound_probability_generator.py |
| `PROB_INDEPENDENT` | 1 | `PROB_INDEPENDENT\|Coin flip and die roll are independent events` | compound_probability_generator.py |
| `PROB_MULTIPLY` | 3 | `PROB_MULTIPLY\|1/2\|1/6\|1/12` | compound_probability_generator.py |
| `PROB_SETUP` | 2 | `PROB_SETUP\|8\|9` | simple_probability_generator.py |
| `PROB_SIMPLIFY` | 2 | *(not observed in sampling)* | compound_probability_generator.py |
| `PROP_SETUP` | 1 | `PROP_SETUP\|12/2 = x/3` | proportion_word_problem_generator.py, proportional_relationship_generator.py, similar_triangles_generator.py, triangle_solve_generator.py |
| `PYTHAG_CALCULATE` | 2 | `PYTHAG_CALCULATE\|d² = 900 + 1600 = 2500\|2500` | pythag_leg_generator.py |
| `PYTHAG_CONTEXT` | 2 | `PYTHAG_CONTEXT\|rectangle_diagonal\|length=30, width=40` | pythag_leg_generator.py |
| `PYTHAG_FORMULA` | 1 | `PYTHAG_FORMULA\|a² + b² = c²` | pythag_leg_generator.py |
| `PYTHAG_MODEL` | 3 | `PYTHAG_MODEL\|length=30\|width=40\|diagonal=?` | pythag_leg_generator.py |
| `PYTHAG_ROOT` | 2 | `PYTHAG_ROOT\|400\|20` | pythag_leg_generator.py |
| `PYTHAG_SETUP` | 3 | `PYTHAG_SETUP\|c=29\|a=21\|b=?` | pythag_leg_generator.py |
| `PYTHAG_SOLVE` | 2 | `PYTHAG_SOLVE\|b² = 841 - 441\|400` | pythag_leg_generator.py |
| `PYTHAG_SQUARE` | 2 | `PYTHAG_SQUARE\|21\|441` | pythag_leg_generator.py |
| `PYTHAG_SUBSTITUTE` | 1 | `PYTHAG_SUBSTITUTE\|21² + b² = 29²` | pythag_leg_generator.py |
| `Q1` | 4 | `Q1\|3\|7\|2\|5` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `Q2` | 4 | `Q2\|3\|7\|2\|-2` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `QUADRANT` | 2 | `QUADRANT\|328°\|quadrant IV` | angle_measure_generator.py, polar_parametric_generator.py, unit_circle_generator.py |
| `QUARTILE` | 3 | `QUARTILE\|Q1\|7,11,17,20,20,25,29\|20` | five_number_summary_generator.py |
| `R` | 1 | `R\|21` | complex_number_ops_generator.py, long_division_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `RATE_MONTHLY` | 2 | `RATE_MONTHLY\|18% / 12\|0.015` | finance_generator.py |
| `RATE_SETUP` | 2 | `RATE_SETUP\|13 ft ladder; the base slides away at 1 ft/s; base is 5 ft from the wall\|dy/dt` | related_rates_generator.py |
| `RATIONALIZE` | 1 | `RATIONALIZE\|(4 - √2)/(4 - √2)` | dot_product_generator.py, limit_evaluation_generator.py, radical_rationalize_generator.py, special_right_triangle_generator.py |
| `RATIO_BASE` | 3 | `RATIO_BASE\|60:55\|5\|12:11` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RATIO_TABLE` | 2 | `RATIO_TABLE\|Red (liters): 60, 72, 96, 132\|Blue (liters): 55, 66, 88, ?` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RAW_FORMULA` | 1 | `RAW_FORMULA\|x = μ + z·σ` | z_score_generator.py |
| `REARRANGE_EQ` | 1 | `REARRANGE_EQ\|whole = 5 / 0.25` | percent_problem_generator.py |
| `RECIPROCAL` | 2 | `RECIPROCAL\|csc θ = 1/sin θ\|-5/3` | trig_six_functions_generator.py |
| `REG_ROW` | 3 | `REG_ROW\|x-x̄=-2\|y-ȳ=-6\|product=12` | regression_generator.py |
| `REG_SETUP` | 2 | `REG_SETUP\|line ŷ = 76.8 + 0.4x\|predict ŷ at x = 7` | regression_generator.py |
| `REJECT` | 2 | `REJECT\|(-1, -45)\|sum is -46, need -14` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `RESID_SETUP` | 2 | `RESID_SETUP\|point (4, 63), line ŷ = 77.1 - 2.7x\|residual = observed − predicted` | regression_generator.py |
| `REVERSE` | 2 | `REVERSE\|1,0,1,0,1,0,0,1\|10010101` | base_arithmetic_generator.py, base_conversion_generator.py |
| `REWRITE` | 1 | `REWRITE\|8 + 90` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, chain_rule_generator.py, circle_equation_generator.py, completing_square_generator.py, complex_division_generator.py, complex_number_ops_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, domain_range_generator.py, dot_product_generator.py, evaluate_expression_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, frequency_table_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, implicit_diff_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, inverse_function_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logistic_growth_generator.py, matrix_inverse_generator.py, midpoint_generator.py, normal_table_generator.py, optimization_generator.py, order_of_operations_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, permutation_combination_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, power_series_generator.py, quadratic_factoring_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, right_triangle_trig_generator.py, row_reduction_generator.py, separable_ode_generator.py, series_convergence_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, u_substitution_generator.py, vector_ops_generator.py |
| `RIEMANN_SETUP` | 2 | `RIEMANN_SETUP\|f(x) = x^2 on [0, 4], n = 4\|right Riemann sum` | riemann_sum_generator.py |
| `ROOT` | 2 | `ROOT\|2601\|51` | completing_square_generator.py, confidence_interval_generator.py, factor_special_forms_generator.py, hypothesis_test_generator.py, pythag_hyp_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, regression_generator.py, round_solids_generator.py |
| `ROOT_EXTRACT` | 2 | `ROOT_EXTRACT\|5` | exponent_generator.py |
| `ROOT_IDENTIFY` | 3 | `ROOT_IDENTIFY\|125\|perfect_cube\|5` | exponent_generator.py |
| `ROOT_SETUP` | 1 | `ROOT_SETUP\|∛125` | exponent_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `ROOT_SIMPLIFY` | 1 | `ROOT_SIMPLIFY\|4√6` | complex_quadratic_generator.py, distance_formula_generator.py, dot_product_generator.py, exponent_generator.py, geometric_mean_generator.py, hypercube_counting_generator.py, polar_parametric_generator.py, vector_ops_generator.py |
| `ROUND_CHECK` | 3 | `ROUND_CHECK\|68867\|100\|>=5` | place_value_rounding_generator.py |
| `ROUND_RESULT` | 2 | `ROUND_RESULT\|68867\|68900` | place_value_rounding_generator.py |
| `ROW_OP` | 2 | `ROW_OP\|R2 → R2 - 2·R1\|[0, 1, -2, -3]` | row_reduction_generator.py |
| `RSQ_FORMULA` | 1 | `RSQ_FORMULA\|r^2 = Sxy^2/(Sxx·Syy)` | regression_generator.py |
| `S` | 3 | `S\|632\|594\|38` | angle_measure_generator.py, arc_length_generator.py, area_between_curves_generator.py, arithmetic_sequence_generator.py, binomial_probability_generator.py, circle_angle_generator.py, circle_equation_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, cramers_rule_generator.py, decimal_div_generator.py, definite_integral_generator.py, determinant_generator.py, distance_formula_generator.py, ellipse_features_generator.py, euler_characteristic_generator.py, euler_method_generator.py, expected_value_generator.py, exponential_model_generator.py, finance_generator.py, five_number_summary_generator.py, fraction_op_generator.py, function_operations_generator.py, geometric_distribution_generator.py, geometric_sequence_generator.py, graph_interpret_generator.py, hyperbola_features_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, kinematics_generator.py, linear_simple_generator.py, logistic_growth_generator.py, long_division_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, normal_table_generator.py, optimization_generator.py, order_of_operations_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, probability_addition_rule_generator.py, radical_add_sub_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, regression_generator.py, related_rates_generator.py, riemann_sum_generator.py, row_reduction_generator.py, segment_partition_generator.py, series_convergence_generator.py, slope_two_points_generator.py, solid_revolution_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py, vector_ops_generator.py, z_score_generator.py |
| `SAMPLE_SIZE_FORMULA` | 1 | `SAMPLE_SIZE_FORMULA\|n = (z*·σ/E)^2` | confidence_interval_generator.py |
| `SA_BASES` | 2 | `SA_BASES\|2π(2)² = 2π × 4\|8π` | volume_3d_generator.py |
| `SA_FACES` | 3 | `SA_FACES\|top/bottom\|12 × 5\|60` | volume_3d_generator.py |
| `SA_FORMULA` | 1 | `SA_FORMULA\|SA = 2(lw + lh + wh)` | round_solids_generator.py, volume_3d_generator.py |
| `SA_LATERAL` | 2 | `SA_LATERAL\|2π × 2 × 5\|20π` | volume_3d_generator.py |
| `SA_SETUP` | 2 | `SA_SETUP\|rectangular_prism\|l=12, w=5, h=5` | volume_3d_generator.py |
| `SA_TOTAL` | 2 | `SA_TOTAL\|SA = 2(60 + 60 + 25)\|290` | round_solids_generator.py, volume_3d_generator.py |
| `SCALE_DIV` | 3 | `SCALE_DIV\|10\|10\|1.0` | scaling_generator.py |
| `SCALE_IDENTIFY` | 2 | `SCALE_IDENTIFY\|1.5 inches\|actual_dimension` | scaling_generator.py |
| `SCALE_MULT` | 3 | `SCALE_MULT\|1.5\|50\|75.0` | scaling_generator.py |
| `SCALE_SETUP` | 3 | `SCALE_SETUP\|1 inch\|50 feet\|50` | scaling_generator.py |
| `SCI_IDENTIFY` | 2 | `SCI_IDENTIFY\|4.0\|5` | exponent_generator.py |
| `SCI_MOVE_DECIMAL` | 2 | `SCI_MOVE_DECIMAL\|left\|5` | exponent_generator.py |
| `SCI_OPERATION` | 4 | `SCI_OPERATION\|multiply_coefficients\|2.3\|2.1\|4.83` | exponent_generator.py |
| `SCI_SETUP` | 1 | `SCI_SETUP\|(2.3 × 10^3) × (2.1 × 10^5)` | exponent_generator.py |
| `SECOND_DERIV_TEST` | 2 | `SECOND_DERIV_TEST\|f''(-1) = -12 < 0\|local maximum at x = -1` | curve_analysis_generator.py, optimization_generator.py |
| `SECTION_FORMULA` | 1 | `SECTION_FORMULA\|P = (x1 + m/(m+n)·(x2 - x1), y1 + m/(m+n)·(y2 - y1))` | segment_partition_generator.py |
| `SECTION_SETUP` | 2 | `SECTION_SETUP\|A(7, 0), B(31, 24); ratio 4:2 from A\|point P` | segment_partition_generator.py |
| `SECTOR_FORMULA` | 1 | `SECTOR_FORMULA\|A = (θ/360)·πr^2` | arc_sector_generator.py |
| `SELECT_RELEVANT` | 2 | `SELECT_RELEVANT\|base = 99, rate = 25%\|ignore 32 (irrelevant)` | percent_word_problem_generator.py, proportion_word_problem_generator.py |
| `SEPARATE` | 1 | `SEPARATE\|y^(-2) dy = dx` | separable_ode_generator.py |
| `SEQ_APPLY` | 1 | `SEQ_APPLY\|-147 = 0 + (n - 1)·-7` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_FORMULA` | 1 | `SEQ_FORMULA\|a_n = a_1 + (n - 1)d` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_SETUP` | 2 | `SEQ_SETUP\|0, -7, -14, -21, ...\|which term equals -147` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SERIES_SETUP` | 2 | `SERIES_SETUP\|Σ (3n + 2)/(n + 4), n ≥ 1\|converge or diverge?` | power_series_generator.py, series_convergence_generator.py |
| `SETUP_PERCENT_EQ` | 1 | `SETUP_PERCENT_EQ\|5 = 0.25 * whole` | percent_problem_generator.py |
| `SIGMA_EXPAND` | 1 | `SIGMA_EXPAND\|7 + 8 + 9 + 10` | sigma_notation_generator.py |
| `SIGMA_SETUP` | 2 | `SIGMA_SETUP\|Σ_(k=1)^(4) (k + 6)\|expand and evaluate` | sigma_notation_generator.py |
| `SIGMA_TERM` | 3 | `SIGMA_TERM\|k=1\|(1) + 6\|7` | sigma_notation_generator.py |
| `SIGN_RULE` | 2 | `SIGN_RULE\|cos, quadrant IV\|positive` | trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `SIMILAR_APPLY` | 3 | `SIMILAR_APPLY\|4\|2\|8` | scaling_generator.py |
| `SIMILAR_SCALE` | 3 | `SIMILAR_SCALE\|10\|5\|2` | scaling_generator.py |
| `SIMILAR_SETUP` | 3 | `SIMILAR_SETUP\|triangle\|4,5,5\|10 (others unknown)` | scaling_generator.py |
| `SIM_SETUP` | 2 | `SIM_SETUP\|△ABC ~ △DEF; AB = 10, DE = 25, BC = 14\|find EF` | similar_triangles_generator.py |
| `SINUSOID_SETUP` | 2 | `SINUSOID_SETUP\|y = 5sin(2(x - π/4)) + 5\|amplitude, period, phase shift, midline` | sinusoid_features_generator.py |
| `SLOPE_CALC` | 2 | *(not observed in sampling)* | equation_from_two_points_generator.py |
| `SLOPE_FORMULA` | 1 | `SLOPE_FORMULA\|m = (y2 - y1) / (x2 - x1)` | equation_from_two_points_generator.py, regression_generator.py, slope_two_points_generator.py |
| `SLOPE_INT_IDENTIFY` | 2 | `SLOPE_INT_IDENTIFY\|Slope (m)\|-2` | slope_intercept_form_generator.py |
| `SLOPE_INT_MATCH` | 2 | `SLOPE_INT_MATCH\|Compare to Slope-Intercept Form\|y = mx + b` | slope_intercept_form_generator.py |
| `SLOPE_INT_SETUP` | 1 | `SLOPE_INT_SETUP\|y = 7 - 2x` | slope_intercept_form_generator.py |
| `SLOPE_RESULT` | 1 | `SLOPE_RESULT\|-5/2` | equation_from_two_points_generator.py |
| `SLOPE_SETUP` | 2 | `SLOPE_SETUP\|(8, -6)\|(-2, 8)` | slope_two_points_generator.py |
| `SLOPE_SUBST` | 1 | `SLOPE_SUBST\|m = (8 - (-6)) / (-2 - 8)` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_UNDEFINED` | 1 | `SLOPE_UNDEFINED\|Division by zero` | slope_two_points_generator.py |
| `SOLUTIONS` | 2 | `SOLUTIONS\|sin x = 1/2\|30°, 150°` | trig_equation_generator.py |
| `SORT` | 2 | `SORT\|8,17,12,2,18,6,8\|2,6,8,8,12,17,18` | five_number_summary_generator.py, simple_stats_generator.py |
| `SPECIAL_SOLUTION` | 2 | `SPECIAL_SOLUTION\|0 = 0\|identity: true for every x` | radical_equation_generator.py, special_solution_equation_generator.py |
| `SPLIT_MIDDLE` | 2 | `SPLIT_MIDDLE\|11x = -x + 12x\|4x^2 - x + 12x - 3` | factor_trinomial_generator.py |
| `SQRT_BOTH_SIDES` | 2 | `SQRT_BOTH_SIDES\|x^2 = 16\|x = ±4` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `SQRT_NEG` | 2 | `SQRT_NEG\|√(-64)\|8i` | complex_quadratic_generator.py, polynomial_zeros_generator.py |
| `SQUARE_BOTH_SIDES` | 2 | `SQUARE_BOTH_SIDES\|√(x + 3) = x + 1\|x + 3 = (x + 1)^2` | radical_equation_generator.py |
| `SQUARE_FACTOR` | 3 | `SQUARE_FACTOR\|44\|4 × 11\|4` | radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `SQUARE_TEST` | 3 | `SQUARE_TEST\|105\|10^2 = 100, 11^2 = 121\|not a perfect square` | discriminant_generator.py |
| `STAT_ABS_DEV` | 2 | `STAT_ABS_DEV\|-8\|8` | statistics_generator.py |
| `STAT_AVERAGE` | 2 | `STAT_AVERAGE\|(61 + 81) / 2\|71.0` | statistics_generator.py |
| `STAT_COUNT` | 1 | `STAT_COUNT\|8` | statistics_generator.py |
| `STAT_DEVIATION` | 3 | `STAT_DEVIATION\|26\|34\|-8` | statistics_generator.py |
| `STAT_DIVIDE` | 2 | `STAT_DIVIDE\|440 / 8\|55` | statistics_generator.py |
| `STAT_FREQUENCY` | 2 | `STAT_FREQUENCY\|12\|2` | statistics_generator.py |
| `STAT_MAD` | 3 | `STAT_MAD\|48\|7\|6.86` | statistics_generator.py |
| `STAT_MAX` | 1 | `STAT_MAX\|94` | statistics_generator.py |
| `STAT_MEAN` | 2 | `STAT_MEAN\|238 / 7\|34` | statistics_generator.py |
| `STAT_MIDDLE` | 2 | `STAT_MIDDLE\|position 5\|73` | statistics_generator.py |
| `STAT_MIN` | 1 | `STAT_MIN\|25` | statistics_generator.py |
| `STAT_MODE` | 2 | `STAT_MODE\|64\|3` | statistics_generator.py |
| `STAT_ORDER` | 1 | `STAT_ORDER\|17, 22, 61, 73, 73, 92, 94, 97, 97` | statistics_generator.py |
| `STAT_RANGE` | 2 | `STAT_RANGE\|94 - 25\|69` | statistics_generator.py |
| `STAT_SETUP` | 1 | `STAT_SETUP\|74, 69, 48, 58, 65, 41, 43, 42` | statistics_generator.py |
| `STAT_SUM` | 2 | `STAT_SUM\|74 + 69 + 48 + 58 + 65 + 41 + 43 + 42\|440` | statistics_generator.py |
| `SUBST` | 3 | `SUBST\|x\|-3\|4(-3)+y-3` | arc_length_generator.py, chain_rule_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, evaluate_expression_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, implicit_diff_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, optimization_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, power_series_generator.py, recursive_explicit_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, separable_ode_generator.py, tangent_line_generator.py, taylor_series_generator.py, trig_equation_generator.py, u_substitution_generator.py |
| `SUB_COL` | 3 | `SUB_COL\|col_1\|5-6-borrow0\|->9 (borrow_out 1)` | multi_digit_subtraction_generator.py |
| `SUM` | 2 | `SUM\|56 + 68 + 65 + 62 + 59\|310` | regression_generator.py |
| `SWAP_VARS` | 1 | `SWAP_VARS\|x = -4y - 7` | inverse_function_generator.py |
| `SYNDIV_SETUP` | 2 | `SYNDIV_SETUP\|x^4 + x^3 - 21x^2 - x + 24\|r = -5` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_DROP` | 1 | `SYN_DROP\|1` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_ROW` | 1 | `SYN_ROW\|1, -4, -1, 4, 4` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYS_ADD` | 1 | `SYS_ADD\|Add equations: -16x = -128` | systems_elimination_generator.py |
| `SYS_EQ_NEW` | 1 | `SYS_EQ_NEW\|New equation with x only` | systems_substitution_generator.py |
| `SYS_ISOLATE` | 2 | `SYS_ISOLATE\|Isolate x in Eq 1\|x = 4y + 13` | systems_substitution_generator.py |
| `SYS_MULT` | 1 | `SYS_MULT\|Eq1 * -5, Eq2 * 2` | systems_elimination_generator.py |
| `SYS_REWRITE` | 2 | `SYS_REWRITE\|-10x + 10y = -110\|-6x - 10y = -18` | systems_elimination_generator.py |
| `SYS_SETUP` | 2 | `SYS_SETUP\|x - 4y = 13\|-5x + 2y = 25` | systems_elimination_generator.py, systems_substitution_generator.py |
| `SYS_SUBST` | 1 | `SYS_SUBST\|Substitute x in Eq 2` | systems_substitution_generator.py |
| `SYS_SUBST_BACK` | 1 | `SYS_SUBST_BACK\|Substitute y=-5 into x = 4y + 13` | systems_elimination_generator.py, systems_substitution_generator.py |
| `TABLE_ENTRY` | 2 | `TABLE_ENTRY\|f(-3)\|-26` | euler_method_generator.py, function_table_generator.py, taylor_series_generator.py |
| `TABLE_LOOKUP` | 2 | `TABLE_LOOKUP\|f(-3)\|26` | dot_product_generator.py, function_evaluation_generator.py, normal_table_generator.py, pascal_triangle_generator.py, polar_parametric_generator.py, right_triangle_trig_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, unit_circle_generator.py |
| `TAYLOR_FORMULA` | 1 | `TAYLOR_FORMULA\|P_n(x) = Σ f^(k)(a)/k!·(x - a)^k` | taylor_series_generator.py |
| `TAYLOR_SETUP` | 2 | `TAYLOR_SETUP\|f(x) = 1/x, center a = 1\|Taylor polynomial of degree 2` | taylor_series_generator.py |
| `TERM` | 2 | `TERM\|i=0: 1·(1/5)^0·(4/5)^4\|0.4096` | binomial_probability_generator.py |
| `TEST_CHOOSE` | 2 | `TEST_CHOOSE\|nth-term test\|always check lim a_n first` | power_series_generator.py, series_convergence_generator.py |
| `TEST_STAT_FORMULA` | 1 | `TEST_STAT_FORMULA\|z = (p̂ - p0)/√(p0(1-p0)/n)` | hypothesis_test_generator.py |
| `THEOREM` | 2 | `THEOREM\|remainder theorem\|remainder on division by x + 2 is P(-2)` | circle_angle_generator.py, geometric_mean_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py, rational_root_generator.py, remainder_factor_theorem_generator.py, series_convergence_generator.py, special_right_triangle_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py |
| `TRANSFORM_APPLY` | 2 | `TRANSFORM_APPLY\|(-(-1), -(-4))\|(1, 4)` | transformation_generator.py |
| `TRANSFORM_RULE` | 1 | `TRANSFORM_RULE\|(x, y) → (-x, -y)` | transformation_generator.py |
| `TRANSFORM_SETUP` | 2 | `TRANSFORM_SETUP\|P(-1, -4)\|rotation 180° about the origin, then reflection over the y-axis` | transformation_generator.py |
| `TRIG_RATIO` | 2 | `TRIG_RATIO\|cos\|adjacent/hypotenuse` | right_triangle_trig_generator.py |
| `TRIG_SETUP` | 2 | `TRIG_SETUP\|right triangle: leg opposite A = 20, leg adjacent to A = 21, hypotenuse = 29\|cos A` | right_triangle_trig_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `TRI_ANGLE_SETUP` | 3 | `TRI_ANGLE_SETUP\|60\|67\|exterior` | angle_relationships_generator.py |
| `TRI_ANGLE_SOLVE` | 2 | `TRI_ANGLE_SOLVE\|exterior = 60 + 67\|127` | angle_relationships_generator.py |
| `TRI_ANGLE_SUM` | 1 | `TRI_ANGLE_SUM\|Exterior angle = sum of remote interior angles` | angle_relationships_generator.py |
| `TRI_AREA_FORMULA` | 1 | `TRI_AREA_FORMULA\|Area = (1/2)·a·b·sin C` | triangle_area_sas_generator.py |
| `TRI_SETUP` | 2 | `TRI_SETUP\|30-60-90 triangle, shorter leg = 12\|longer leg and hypotenuse` | special_right_triangle_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py |
| `TRY` | 2 | `TRY\|(-1, -45)\|(-1)·(-45)=45, (-1)+(-45)=-46` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `TWOS_SETUP` | 2 | `TWOS_SETUP\|8-bit two's complement\|offset = 2^8 = 256` | base_conversion_generator.py |
| `UC_POINT` | 2 | `UC_POINT\|180°\|(-1, 0)` | unit_circle_generator.py |
| `UNIT_ATTACH` | 3 | `UNIT_ATTACH\|308\|feet\|308 feet` | kinematics_generator.py, physics_formula_generator.py |
| `UNIT_CONVERT` | 2 | `UNIT_CONVERT\|6 minutes\|360 seconds` | physics_formula_generator.py |
| `UNIT_RATE_DIV` | 3 | `UNIT_RATE_DIV\|$20.00\|10\|$2.00` | unit_rate_generator.py |
| `UNIT_RATE_PICK` | 2 | `UNIT_RATE_PICK\|1\|8` | unit_rate_generator.py |
| `UNIT_RATE_SETUP` | 3 | `UNIT_RATE_SETUP\|10\|pounds\|$20.00` | unit_rate_generator.py |
| `UNIT_RATE_TABLE` | 2 | `UNIT_RATE_TABLE\|1,4,7,8\|8,32,56,64` | unit_rate_generator.py |
| `UNLIKE_RADICALS` | 2 | `UNLIKE_RADICALS\|√2 ≠ √5\|unlike radicands — cannot combine` | radical_add_sub_generator.py |
| `UNROLL` | 2 | `UNROLL\|5, -10, 20, -40\|geometric, r = -2` | recursive_explicit_generator.py |
| `VA` | 1 | `VA\|x = -4` | rational_function_features_generator.py |
| `VAR_FORMULA` | 1 | `VAR_FORMULA\|Var(X) = Σ P(x)·(x - μ)^2` | expected_value_generator.py |
| `VAR_ROW` | 3 | `VAR_ROW\|1 - 3.8 = -2.8\|(-2.8)^2 = 7.84\|1/10·7.84 = 0.784` | expected_value_generator.py |
| `VEC_SETUP` | 2 | `VEC_SETUP\|u = ⟨4, 3⟩, v = ⟨-1, -2⟩\|3u + 3v` | dot_product_generator.py, vector_ops_generator.py |
| `VERIFY` | 2 | `VERIFY\|1\|ok` | error_spotting_generator.py |
| `VERTEX` | 1 | `VERTEX\|(-2, 4)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `VOLUME` | 1 | `VOLUME\|385` | volume_rect_prism_generator.py |
| `VOLUME_SETUP` | 2 | `VOLUME_SETUP\|region between y = 2x (outer) and y = 2x^2 (inner) on [0, 1], about the x-axis\|washer method` | solid_revolution_generator.py |
| `VOL_BASE_AREA` | 2 | `VOL_BASE_AREA\|Base Area = (1/2) × 12 × 8\|48.0` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_CALCULATE` | 2 | `VOL_CALCULATE\|V = 3 × 11 × 5\|165` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_FORMULA` | 1 | `VOL_FORMULA\|V = l × w × h` | round_solids_generator.py, solid_revolution_generator.py, volume_3d_generator.py |
| `VOL_SETUP` | 2 | `VOL_SETUP\|rectangular_prism\|l=3, w=11, h=5` | volume_3d_generator.py |
| `Z` | 1 | `Z\|63 R84` | abacus_addition_generator.py, absolute_value_equation_generator.py, absolute_value_inequality_generator.py, angle_measure_generator.py, angle_relationships_generator.py, antiderivative_generator.py, arc_length_generator.py, arc_sector_generator.py, area_between_curves_generator.py, arithmetic_sequence_generator.py, base_arithmetic_generator.py, base_conversion_generator.py, binomial_probability_generator.py, chain_rule_generator.py, chi_square_generator.py, circle_angle_generator.py, circle_equation_generator.py, circle_generator.py, completing_square_generator.py, complex_division_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, compound_inequality_generator.py, compound_probability_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, decimal_add_sub_generator.py, decimal_div_generator.py, decimal_mult_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dimensional_analysis_generator.py, discriminant_generator.py, distance_formula_generator.py, divisibility_classification_generator.py, domain_range_generator.py, dot_product_generator.py, ellipse_features_generator.py, equation_from_two_points_generator.py, error_spotting_generator.py, euler_characteristic_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, factors_generator.py, fill_in_step_generator.py, finance_generator.py, five_number_summary_generator.py, fraction_comparison_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, gcf_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, implicit_diff_generator.py, improper_integral_generator.py, integer_operations_generator.py, integration_by_parts_generator.py, inverse_function_generator.py, kinematics_generator.py, lcm_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, linear_simple_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logistic_growth_generator.py, long_division_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, monomial_mult_div_generator.py, multi_digit_addition_generator.py, multi_digit_multiplication_generator.py, multi_digit_subtraction_generator.py, multi_step_unit_conversion_generator.py, multiplying_binomials_generator.py, multiplying_polynomials_generator.py, nets_surface_area_generator.py, normal_table_generator.py, number_comparison_generator.py, one_step_equation_generator.py, one_step_inequality_generator.py, optimization_generator.py, order_of_operations_generator.py, parabola_features_generator.py, parallel_perpendicular_line_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, pascal_triangle_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, permutation_combination_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, place_value_rounding_generator.py, point_slope_generator.py, polar_parametric_generator.py, polygon_perimeter_generator.py, polynomial_add_sub_generator.py, polynomial_div_monomial_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, power_series_generator.py, prime_factorization_generator.py, probability_addition_rule_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, pythag_hyp_generator.py, pythag_leg_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, rational_root_generator.py, recursive_explicit_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, repeating_decimal_generator.py, riemann_sum_generator.py, right_triangle_trig_generator.py, round_solids_generator.py, row_reduction_generator.py, scaling_generator.py, segment_partition_generator.py, separable_ode_generator.py, series_convergence_generator.py, sigma_notation_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simple_stats_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, slope_intercept_form_generator.py, slope_two_points_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, standard_deviation_generator.py, standard_form_conversion_generator.py, statistics_generator.py, synthetic_division_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, two_step_equation_generator.py, two_step_inequality_generator.py, u_substitution_generator.py, unit_circle_generator.py, unit_conversion_generator.py, unit_rate_generator.py, vector_ops_generator.py, volume_3d_generator.py, volume_rect_prism_generator.py, z_score_generator.py |
| `ZERO_PRODUCT` | 2 | `ZERO_PRODUCT\|4n(n - 3) = 0\|4n = 0 or n - 3 = 0` | area_between_curves_generator.py, curve_analysis_generator.py, domain_range_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_zeros_generator.py, quadratic_factoring_generator.py, radical_equation_generator.py, trig_equation_generator.py |
| `ZSCORE` | 2 | `ZSCORE\|(54 - 44)/4\|2.5` | normal_table_generator.py, z_score_generator.py |
| `ZSCORE_FORMULA` | 1 | `ZSCORE_FORMULA\|z = (x - μ)/σ` | z_score_generator.py |
