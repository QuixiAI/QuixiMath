# Op-Code Legend

**Generated file — do not hand-edit.** Regenerate with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and this legend is *descriptive*, not prescriptive. Steps are pipe-delimited strings (`CODE|field|field|...`, at most 4 payload fields) built with `helpers.step()`; the final step of every problem is `Z|<final_answer>`.

1795 distinct op-codes observed.

| Code | Payload fields | Example | Used by |
|---|---|---|---|
| `A` | 2, 3 | `A\|46\|46\|92` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, algorithm_trace_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, base_conversion_generator.py, bayesian_update_generator.py, binomial_probability_generator.py, bisection_generator.py, bond_pricing_generator.py, branching_ratio_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_generator.py, cayley_table_generator.py, channel_capacity_generator.py, chi_square_generator.py, circle_equation_generator.py, classifier_metrics_generator.py, collision_generator.py, commutator_generator.py, complement_probability_generator.py, complex_division_generator.py, complex_locus_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continued_fraction_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, countability_bijection_generator.py, counterexample_search_generator.py, counting_classics_generator.py, crt_generator.py, curve_analysis_generator.py, cyclic_group_generator.py, de_moivre_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dft_generator.py, dijkstra_generator.py, distance_formula_generator.py, doppler_generator.py, dot_product_generator.py, dp_table_generator.py, einstein_summation_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equivalence_relation_generator.py, euler_characteristic_generator.py, euler_formula_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, feature_map_generator.py, fill_in_step_generator.py, finance_generator.py, finite_field_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_inner_product_generator.py, function_operations_generator.py, function_table_generator.py, game_theory_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_mean_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, heat_engine_generator.py, hermitian_check_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, information_gain_generator.py, integers_as_pairs_generator.py, integrating_factor_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, layer_norm_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_calculus_generator.py, matrix_group_check_generator.py, matrix_norm_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, modular_arithmetic_generator.py, mst_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, nets_surface_area_generator.py, newtons_laws_generator.py, npv_irr_generator.py, odds_probability_generator.py, operation_properties_generator.py, or_formula_generator.py, order_of_operations_generator.py, order_statistics_generator.py, ordinal_arithmetic_generator.py, parabola_features_generator.py, param_count_generator.py, partition_function_generator.py, pascal_triangle_generator.py, pca_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_group_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, polygon_perimeter_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, probability_addition_rule_generator.py, probability_axioms_finite_generator.py, probability_measure_generator.py, pythag_hyp_generator.py, quantization_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, rational_expr_add_sub_generator.py, rationals_as_pairs_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regression_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, segment_partition_generator.py, separable_pde_generator.py, set_counting_generator.py, shm_generator.py, sigma_notation_generator.py, simple_stats_generator.py, simplex_generator.py, softmax_gradient_generator.py, solution_chem_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, standard_deviation_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, svm_margin_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transfer_function_generator.py, transformation_generator.py, transportation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, two_way_table_probability_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py, vector_ops_generator.py, venn_probability_generator.py, venn_region_count_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `ABS` | 2 | `ABS\|1/9\|1/9` | fixed_point_generator.py, matrix_norm_generator.py, rv_transform_generator.py |
| `ABSORB_EQ` | 2 | `ABSORB_EQ\|u0=p0A+p00*u0+p01*u1\|u1=p1A+p10*u0+p11*u1` | markov_chain_generator.py |
| `ABS_CASE` | 2 | `ABS_CASE\|Case 1\|5x + 7 = 11` | absolute_value_equation_generator.py |
| `ABS_CHECK` | 2 | `ABS_CHECK\|-4 < 0\|Absolute value cannot be negative` | absolute_value_equation_generator.py |
| `ABS_ERROR` | 2 | `ABS_ERROR\|1\|1/100` | quantization_generator.py |
| `ABS_INEQ_CHECK` | 2 | `ABS_INEQ_CHECK\|-2 < 0\|Absolute value is always non-negative` | absolute_value_inequality_generator.py |
| `ABS_INEQ_PART` | 2 | `ABS_INEQ_PART\|Part 1\|5x - 10 > 3 -> x > 13/5` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SETUP` | 1 | `ABS_INEQ_SETUP\|abs(x + 6) ≤ 8` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPECIAL` | 2 | `ABS_INEQ_SPECIAL\|c = 0\|Check logic for >=` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPLIT` | 2 | `ABS_INEQ_SPLIT\|AND case\|-8 ≤ x + 6 ≤ 8` | absolute_value_inequality_generator.py |
| `ABS_SETUP` | 1 | `ABS_SETUP\|abs(5x + 7) = 11` | absolute_value_equation_generator.py |
| `ABS_SPLIT` | 2, 3 | `ABS_SPLIT\|Two cases\|5x + 7 = 11\|5x + 7 = -11` | absolute_value_equation_generator.py |
| `ABS_VAL` | 2 | `ABS_VAL\|13\|13` | taxicab_geometry_generator.py |
| `AB_ADD` | 3 | `AB_ADD\|+4000\|5230\|9230` | abacus_addition_generator.py |
| `AB_SET` | 1 | `AB_SET\|5230` | abacus_addition_generator.py |
| `ACCEPT` | 1, 2 | `ACCEPT\|x = −22` | conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, knights_knaves_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py, structure_isomorphism_generator.py |
| `ACT_DERIV` | 3 | `ACT_DERIV\|sigmoid\|0\|1/4` | activation_generator.py |
| `ACT_SETUP` | 3 | `ACT_SETUP\|activation=sigmoid\|x=-5\|w1=-3,b1=-15,w2=-1,b2=0` | activation_generator.py |
| `ACT_VALUE` | 3 | `ACT_VALUE\|sigmoid\|0\|1/2` | activation_generator.py |
| `AC_COMPLEX` | 3 | `AC_COMPLEX\|Z\|1\|0j` | ac_circuit_generator.py |
| `AC_FORMULA` | 1 | `AC_FORMULA\|omega0^2=1/(L*C)` | ac_circuit_generator.py |
| `AC_PRODUCT` | 2 | `AC_PRODUCT\|6 × 10\|60` | factor_trinomial_generator.py |
| `AC_SETUP` | 3 | `AC_SETUP\|resonance\|R=1, L=6\|C=1/150` | ac_circuit_generator.py |
| `ADAM_SETUP` | 3 | `ADAM_SETUP\|theta=3,g=7\|beta1=9/10,beta2=99/100\|lr=1/20,epsilon=0` | adam_step_generator.py |
| `ADAM_UPDATE` | 2 | `ADAM_UPDATE\|theta_new\|59/20` | adam_step_generator.py |
| `ADD_COL` | 3 | `ADD_COL\|col_1\|0+0+0\|->0 (carry 0)` | multi_digit_addition_generator.py |
| `ADD_FORMULA` | 1 | `ADD_FORMULA\|P(A ∩ B) = P(A) + P(B) - P(A ∪ B)` | probability_addition_rule_generator.py |
| `ADD_PARTIALS` | 2 | `ADD_PARTIALS\|410370 + 3419750 + 61555500 + 68395000\|133780620` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `ADD_SETUP` | 2 | `ADD_SETUP\|P(A) = 7/12, P(B) = 6/12, P(A ∪ B) = 8/12\|P(A ∩ B)` | probability_addition_rule_generator.py |
| `ADJOINT` | 1 | `ADJOINT\|A^dagger=[[2,0],[0,2]]` | hermitian_check_generator.py |
| `ADJ_LIST` | 2 | `ADJ_LIST\|A\|B, D` | euler_circuit_generator.py, graph_traversal_generator.py |
| `ALG_SETUP` | 3 | `ALG_SETUP\|merge sort\|merges 3\|values 31, 8, 20, 41, 47` | algorithm_trace_generator.py |
| `ALIGN_NUM` | 2 | `ALIGN_NUM\|046.36\|177.07` | number_comparison_generator.py |
| `ALPHA` | 2 | `ALPHA\|line 2\|4: ¬e; 5: ¬b` | kernel_ridge_generator.py, semantic_tableau_generator.py |
| `ALPHA_RENAME` | 2 | `ALPHA_RENAME\|lambda p. n\|lambda z. n` | lambda_reduction_generator.py |
| `AMORT_ROW` | 3 | `AMORT_ROW\|1\|interest=$44720.00\|principal=$1984.00,balance=$87456.00` | annuity_generator.py |
| `AMPLITUDE` | 2 | `AMPLITUDE\|abs(-2)\|2` | sinusoid_features_generator.py |
| `ANALOGY_SETUP` | 3 | `ANALOGY_SETUP\|man=(-2,-4)\|woman=(-4,-4)\|king=(-5,-4)` | embedding_similarity_generator.py |
| `ANALOGY_VECTOR` | 2 | `ANALOGY_VECTOR\|king-man+woman\|(-7,-4)` | embedding_similarity_generator.py |
| `ANGLE` | 2 | `ANGLE\|theta\|3pi/2` | positional_encoding_generator.py |
| `ANGLE_DEFECT_SETUP` | 2 | `ANGLE_DEFECT_SETUP\|R=20\|angles=45,45,15` | angle_defect_generator.py |
| `ANGLE_EVAL` | 2 | `ANGLE_EVAL\|theta=0..2*pi\|2*pi` | triple_integral_generator.py |
| `ANGLE_FORMULA` | 1 | `ANGLE_FORMULA\|degrees = radians · 180/π` | angle_measure_generator.py |
| `ANGLE_RELATION` | 1 | `ANGLE_RELATION\|angle1 + angle2 = 90°` | angle_relationships_generator.py |
| `ANGLE_SETUP` | 2 | `ANGLE_SETUP\|complementary\|angle1 = 40°` | angle_relationships_generator.py |
| `ANGLE_SOLVE` | 2 | `ANGLE_SOLVE\|90 - 40\|50` | angle_relationships_generator.py |
| `ANGLE_WRAP` | 2 | `ANGLE_WRAP\|188 deg\|-172 deg` | complex_log_generator.py |
| `ANNUITY_FORMULA` | 1 | `ANNUITY_FORMULA\|FV = PMT*((1+r)^n - 1)/r` | annuity_generator.py |
| `ANNUITY_SETUP` | 2, 3 | `ANNUITY_SETUP\|ordinary annuity future value\|PMT=4585,r=18%,n=2` | annuity_generator.py |
| `ANTICHAIN` | 2 | `ANTICHAIN\|{6, 13, 34}\|size 3` | partial_order_generator.py |
| `ANTICOMM_ENTRY` | 3 | `ANTICOMM_ENTRY\|(1,1)\|0 + 0\|0` | pauli_algebra_generator.py |
| `ANTIDERIV` | 2 | `ANTIDERIV\|-12 cos(4x)\|-3 sin(4x)` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, definite_integral_generator.py, improper_integral_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, ode_substitution_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py, variation_parameters_generator.py |
| `ANTIDERIVATIVE` | 1 | `ANTIDERIVATIVE\|-A*cos(nx)/n` | fourier_series_generator.py |
| `ANTISYM_CHECK` | 3 | `ANTISYM_CHECK\|(1, 3)\|reverse (3, 1)\|ok` | relation_check_generator.py |
| `APPLY` | 3 | `APPLY\|∧I\|1,2\|c ∧ h` | natural_deduction_generator.py |
| `APPLY_GATE` | 3 | `APPLY_GATE\|H\|e^(i51π/91)·ket1\|e^(i51π/91)·(ket0 - ket1)/sqrt(2)` | quantum_gate_generator.py |
| `APPLY_OPERATOR` | 2 | `APPLY_OPERATOR\|L[Ae^(2x)]\|A(4 + 8 + 3)e^(2x)` | commutator_generator.py, undetermined_coeff_generator.py |
| `APPLY_PAULI` | 2 | `APPLY_PAULI\|sigma_z psi\|[3/5,-4/5]` | spin_half_generator.py |
| `APPLY_SUBST` | 1 | *(not observed in sampling)* | unification_generator.py |
| `APPROX` | 2 | `APPROX\|12*d^2*L\|2042413056` | param_count_generator.py |
| `APPROX_ENTRY` | 2 | `APPROX_ENTRY\|(1,1)\|0` | low_rank_approx_generator.py |
| `APPROX_SETUP` | 2 | `APPROX_SETUP\|estimate (2.05)^3\|linearize f(x) = x^3 at a = 2` | linear_approx_generator.py |
| `ARCCOS` | 2 | `ARCCOS\|cos(c)=-1\|c=pi` | great_circle_generator.py |
| `ARCLEN_FORMULA` | 1 | `ARCLEN_FORMULA\|L = ∫ √((dx/dt)^2 + (dy/dt)^2) dt` | arc_length_generator.py, parametric_calculus_generator.py |
| `ARC_FORMULA` | 1 | `ARC_FORMULA\|L = (θ/360)·2πr` | arc_sector_generator.py |
| `ARC_LENGTH` | 3 | `ARC_LENGTH\|int_0^T speed dt\|13*10\|130` | curve_geometry_generator.py |
| `ARC_SETUP` | 2 | `ARC_SETUP\|circle r = 54, central angle 95°\|arc length` | arc_sector_generator.py |
| `AREA` | 1 | `AREA\|66` | geometry_area_perimeter_generator.py |
| `AREA_INT` | 3 | `AREA_INT\|A = int y dx\|3*17^2/2\|867/2` | centroid_generator.py |
| `AREA_INTEGRAL` | 2 | `AREA_INTEGRAL\|sqrt(EG-F^2)=R\|area = R*theta*h` | fundamental_form_generator.py |
| `AREA_SCALE` | 3 | `AREA_SCALE\|uv rectangle area\|7*7\|49` | jacobian_generator.py |
| `AREA_SETUP` | 2 | `AREA_SETUP\|y = x^2 + 2x + 12 and y = -7x - 8\|area between the curves` | area_between_curves_generator.py |
| `ARGUMENT` | 2 | `ARGUMENT\|(0,-11)\|270 deg` | complex_log_generator.py, euler_formula_generator.py |
| `ARG_SETUP` | 2 | `ARG_SETUP\|((r ∧ s) ∧ r) → ¬(s ∨ r); ¬((r ∧ s) ∧ r)\|¬¬(s ∨ r)` | argument_form_generator.py |
| `ARITH_INTERVAL` | 1 | `ARITH_INTERVAL\|[5/8,3/4)` | arithmetic_coding_generator.py |
| `ARITH_SETUP` | 2 | `ARITH_SETUP\|A=1/2, B=1/8, C=1/8, D=1/4\|message=CCB` | arithmetic_coding_generator.py |
| `ARITH_SYMBOL` | 2 | `ARITH_SYMBOL\|C\|cum=[5/8,3/4)` | arithmetic_coding_generator.py |
| `ARRAY_STATE` | 2 | `ARRAY_STATE\|pass 1\|24, 39, 25, 28, 36, 38, 32` | algorithm_trace_generator.py |
| `ASSIGN` | 2 | `ASSIGN\|P1\|C2` | kmeans_step_generator.py |
| `ASSUME` | 1 | `ASSUME\|assume n is odd` | direct_proof_algebra_generator.py, induction_verify_generator.py |
| `ASYMPTOTE` | 1 | `ASYMPTOTE\|y = -2 ± 5(x - 5)` | hyperbola_features_generator.py |
| `ATA` | 2 | `ATA\|A^T A\|[[1769, 1480], [1480, 1769]]` | svd_generator.py |
| `ATOM_CHECK` | 3 | `ATOM_CHECK\|Al\|left=4\|right=4` | stoichiometry_generator.py |
| `ATTN_OUTPUT` | 2 | `ATTN_OUTPUT\|1\|[[-13/3,4]]` | attention_generator.py |
| `ATTN_SCORE` | 2 | `ATTN_SCORE\|1,1\|0` | attention_generator.py |
| `ATTN_SETUP` | 1, 3 | `ATTN_SETUP\|tokens=3,d=2\|Q=[[0,0], [0,0], [0,0]]\|K=[[0,0], [0,0], [0,0]]` | attention_generator.py |
| `ATTR_CHECK` | 3 | `ATTR_CHECK\|4\|A: odd\|no` | attribute_sorting_generator.py |
| `AV_VECTOR` | 2 | `AV_VECTOR\|A*v1\|[57/√2, 57/√2]` | svd_generator.py |
| `AXIOM` | 2 | `AXIOM\|total probability\|Σ P(ω) = 1` | probability_axioms_finite_generator.py, probability_measure_generator.py |
| `AXIOM_MATCH` | 2 | `AXIOM_MATCH\|L3\|p := (¬b ∨ (g → a)), q := ¬¬k` | hilbert_axiom_derivation_generator.py |
| `B` | 1, 3 | `B\|38\|1\|381` | decimal_div_generator.py, long_division_generator.py, percent_problem_generator.py, polynomial_long_division_generator.py |
| `BABY_STEP` | 2 | `BABY_STEP\|j=0\|1` | baby_step_giant_step_generator.py |
| `BACKPROP_DELTA` | 2 | `BACKPROP_DELTA\|h1\|delta=0` | backprop_generator.py |
| `BACKPROP_GRAD` | 2 | `BACKPROP_GRAD\|dL/dy_hat\|-13` | backprop_generator.py |
| `BACKPROP_SETUP` | 3 | `BACKPROP_SETUP\|x=(1,3)\|y=-2\|eta=1/7` | backprop_generator.py |
| `BACK_SUB` | 2 | `BACK_SUB\|v = y/x\|y/x = -3 ln(x) + C` | ode_substitution_generator.py |
| `BACK_SUB_ROW` | 3 | `BACK_SUB_ROW\|r=48\|x=1\|y=0` | extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `BALANCED_EQ` | 1 | `BALANCED_EQ\|4 Al + 3 O2 -> 2 Al2O3` | stoichiometry_generator.py |
| `BALANCE_COEFFS` | 2 | `BALANCE_COEFFS\|reactants=4,3\|products=2` | stoichiometry_generator.py |
| `BASE` | 2 | `BASE\|gcd(1, 0)\|1` | recursive_definition_unfold_generator.py |
| `BASE_ADD_COL` | 3 | `BASE_ADD_COL\|col 0\|F + 7 + carry 0\|22 -> digit 6, carry 1` | base_arithmetic_generator.py |
| `BASE_ARITH_SETUP` | 2 | `BASE_ARITH_SETUP\|base 16\|303 * 5` | base_arithmetic_generator.py |
| `BASE_CARRY` | 2 | `BASE_CARRY\|carry 1\|digit 1, carry 0` | base_arithmetic_generator.py |
| `BASE_MUL_COL` | 3 | `BASE_MUL_COL\|col 0\|3 * 5 + carry 0\|15 -> digit F, carry 0` | base_arithmetic_generator.py |
| `BASE_SETUP` | 2 | `BASE_SETUP\|C1D_16\|decimal` | base_conversion_generator.py |
| `BAYES_CELL` | 3 | `BAYES_CELL\|true positive\|80 * 9/10\|72` | conditional_probability_generator.py |
| `BAYES_FORMULA` | 1 | `BAYES_FORMULA\|P(disease=no given negative) = TN/(TN + FN)` | conditional_probability_generator.py |
| `BAYES_SETUP` | 3 | `BAYES_SETUP\|disease=yes 80, disease=no 200\|sensitivity 9/10, specificity 19/20\|P(disease=no given test negative)` | conditional_probability_generator.py |
| `BAYES_UPDATE_SETUP` | 2, 3 | `BAYES_UPDATE_SETUP\|normal_normal\|prior=Normal(-4,10)\|sigma^2=4` | bayesian_update_generator.py |
| `BCH_FORM` | 2 | `BCH_FORM\|A+B+1/2[A,B]\|[[0, 4, -10], [0, 0, -5], [0, 0, 0]]` | bch_generator.py |
| `BCH_SETUP` | 3 | `BCH_SETUP\|A=4E12\|B=-5E23\|order=2` | bch_generator.py |
| `BEC_FORMULA` | 1 | `BEC_FORMULA\|C=1-epsilon` | bec_channel_generator.py |
| `BEC_SETUP` | 1 | `BEC_SETUP\|epsilon=1/2` | bec_channel_generator.py |
| `BELL_ROW` | 3 | `BELL_ROW\|n=1\|1\|1` | set_counting_generator.py |
| `BEREZIN_RULE` | 2 | `BEREZIN_RULE\|int dtheta 1\|0` | grassmann_generator.py |
| `BETA` | 1, 3 | `BETA\|line 1\|1L: 2: ¬e ∧ ¬b\|1R: 3: ¬q` | lambda_reduction_generator.py, semantic_tableau_generator.py |
| `BETA_COUNT` | 1 | `BETA_COUNT\|2` | lambda_reduction_generator.py |
| `BEZOUT_CHECK` | 2 | `BEZOUT_CHECK\|48*-8 + 35*11\|1` | extended_euclid_generator.py |
| `BIAS_CORRECT` | 2 | `BIAS_CORRECT\|m_hat\|7` | adam_step_generator.py |
| `BIJECTION_RULE` | 2 | `BIJECTION_RULE\|0\|a/b → a/(a + b)` | countability_bijection_generator.py |
| `BINARY` | 2 | `BINARY\|47302\|1011100011000110` | countability_bijection_generator.py |
| `BINARY_EXPONENT` | 2 | `BINARY_EXPONENT\|25\|11001` | mod_exp_generator.py, quadratic_residue_generator.py |
| `BINOM_FORMULA` | 1 | `BINOM_FORMULA\|P(X=k) = C(n,k)·p^k·(1-p)^(n-k)` | binomial_probability_generator.py |
| `BINOM_SETUP` | 2 | `BINOM_SETUP\|n = 3, k = 1, p = 1/4\|P(X = k)` | binomial_probability_generator.py |
| `BISECTION_SETUP` | 3 | `BISECTION_SETUP\|f(x)=x^2-33\|interval=[5, 6]\|iterations=5` | bisection_generator.py |
| `BISECT_UPDATE` | 3 | `BISECT_UPDATE\|1\|product > 0\|[11/2, 6]` | bisection_generator.py |
| `BIT` | 1, 2 | `BIT\|a\|A=0` | characteristic_vector_generator.py |
| `BITWISE` | 1 | `BITWISE\|∨\|110000111\|101110010\|111110111` | characteristic_vector_generator.py |
| `BIT_ROW` | 2, 3 | `BIT_ROW\|0 AND 0\|0` | bitwise_ops_generator.py |
| `BIT_RULE` | 2 | `BIT_RULE\|AND\|1 only when both bits are 1` | bitwise_ops_generator.py |
| `BIT_SETUP` | 2 | `BIT_SETUP\|truth table for AND\|all 2-bit inputs` | bitwise_ops_generator.py |
| `BLACKBODY_FORMULA` | 1 | `BLACKBODY_FORMULA\|P=sigma*A*T^4` | blackbody_generator.py |
| `BLACKBODY_SETUP` | 3 | `BLACKBODY_SETUP\|stefan_power\|sigma=2, A=16\|T=16` | blackbody_generator.py |
| `BOND_FORMULA` | 1 | `BOND_FORMULA\|price=sum coupon/(1+y)^t + face/(1+y)^n` | bond_pricing_generator.py |
| `BOND_PRICE` | 1 | `BOND_PRICE\|$4569.60` | bond_pricing_generator.py |
| `BOND_SETUP` | 2 | `BOND_SETUP\|face=5100\|coupon=12%,ytm=25%,years=1` | bond_pricing_generator.py |
| `BOOL_SETUP` | 2 | `BOOL_SETUP\|variables J, K, L, M\|DNF from F=1 rows` | boolean_algebra_generator.py |
| `BORROW` | 3 | `BORROW\|col_1\|from_left\|1` | multi_digit_subtraction_generator.py |
| `BOX_FORMULA` | 1 | `BOX_FORMULA\|E_n=n^2*h^2/(8*m*L^2)` | particle_in_box_generator.py |
| `BOX_SETUP` | 1, 3 | `BOX_SETUP\|energy_level\|n=2, h=12\|m=9, L=5` | particle_in_box_generator.py |
| `BRAKET_FORMULA` | 1 | `BRAKET_FORMULA\|inner(phi,psi)=sum conj(phi_k)*psi_k` | braket_generator.py |
| `BRAKET_SETUP` | 3 | `BRAKET_SETUP\|inner_product\|phi=[2-i,-2]\|psi=[1,1+i]` | braket_generator.py |
| `BRANCH_CLOSE` | 2 | `BRANCH_CLOSE\|1RL\|s, ¬s` | semantic_tableau_generator.py |
| `BRANCH_OPEN` | 2 | `BRANCH_OPEN\|1L\|b=F, e=F, q=F` | semantic_tableau_generator.py |
| `BRANCH_SUM` | 3 | `BRANCH_SUM\|SF + FS\|5/42 + 5/12\|15/28` | tree_diagram_probability_generator.py |
| `BRANCH_TEST` | 2 | `BRANCH_TEST\|194 <= 100\|no` | piecewise_evaluation_generator.py |
| `BRANCH_USE` | 1 | `BRANCH_USE\|$4.00` | piecewise_evaluation_generator.py |
| `BRING_DOWN` | 2 | `BRING_DOWN\|group 29\|current = 29` | composite_arithmetic_generator.py, manual_square_root_generator.py |
| `BSC_FORMULA` | 1 | `BSC_FORMULA\|H_b=p*(-log2 p)+(1-p)*(-log2(1-p))` | channel_capacity_generator.py |
| `BSC_SETUP` | 3 | `BSC_SETUP\|p=19/100\|-log2(p)=2.396\|-log2(1-p)=0.304` | channel_capacity_generator.py |
| `BSGS_MATCH` | 3 | `BSGS_MATCH\|i=4\|j=4\|x=28` | baby_step_giant_step_generator.py |
| `BSGS_SETUP` | 4 | `BSGS_SETUP\|p=31\|g=3\|h=7\|m=6` | baby_step_giant_step_generator.py |
| `BS_FORMULA` | 2 | `BS_FORMULA\|C=S*N(d1)-K*df*N(d2)\|P=K*df*N(-d2)-S*N(-d1)` | black_scholes_generator.py |
| `BS_RESULT` | 2 | `BS_RESULT\|call=12\|put=4.5` | black_scholes_generator.py |
| `BS_SETUP` | 3 | `BS_SETUP\|S=150,K=150\|df=0.95\|N_d1=0.65,N_d2=0.6` | black_scholes_generator.py |
| `C` | 3 | `C\|1/3\|21\|7/21` | complement_probability_generator.py, experimental_probability_generator.py, fraction_comparison_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `CALC` | 1 | `CALC\|y = 2` | systems_elimination_generator.py, systems_substitution_generator.py |
| `CAL_DIVMOD` | 3 | `CAL_DIVMOD\|119\|7\|17 R0` | calendar_arithmetic_generator.py |
| `CAL_FORMULA` | 1 | `CAL_FORMULA\|q=m*c*(T2-T1)` | calorimetry_generator.py |
| `CAL_SETUP` | 3 | `CAL_SETUP\|2028-09-18\|Monday, offset 1 day\|weekday` | calendar_arithmetic_generator.py, calorimetry_generator.py |
| `CANCEL` | 2 | `CANCEL\|6x\|6x - 7` | derivative_limit_def_generator.py, derivative_transcendental_generator.py, limit_evaluation_generator.py, power_series_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, series_convergence_generator.py, trig_identity_verify_generator.py |
| `CANDIDATES` | 1 | `CANDIDATES\|±1/2, ±1, ±2` | rational_root_generator.py |
| `CANONICAL_ORDER` | 1 | `CANONICAL_ORDER\|B=1, A=2, C=3` | kraft_inequality_generator.py |
| `CANONICAL_SHIFT` | 3 | `CANONICAL_SHIFT\|code=0\|left=1\|0` | kraft_inequality_generator.py |
| `CARD_RULE` | 2 | `CARD_RULE\|set construction\|removing a countable subset from ℝ leaves cardinal c, and a positive finite power of c is c` | cardinal_arithmetic_generator.py |
| `CARRY_FINAL` | 1 | `CARRY_FINAL\|1` | multi_digit_addition_generator.py |
| `CARTESIAN_RESULT` | 1 | `CARTESIAN_RESULT\|{(j, 2), (j, 3), (j, 12), (n, 2), (n, 3), (n, 12), (q, 2), (q, 3), (q, 12)}` | set_operations_generator.py |
| `CART_PAIR` | 3 | `CART_PAIR\|j\|2\|(j, 2)` | set_operations_generator.py |
| `CASE` | 1, 2 | `CASE\|Pia=knight, Oona=knight` | countability_bijection_generator.py, knights_knaves_generator.py |
| `CASHFLOW_PV` | 2 | `CASHFLOW_PV\|coupon_t1\|489.6` | bond_pricing_generator.py |
| `CASIMIR_FORCE_SETUP` | 2 | `CASIMIR_FORCE_SETUP\|F/A=-π^2*hbar*c/(240*d^4)\|hbar=5,c=7,d=2` | casimir_force_generator.py |
| `CASIMIR_SETUP` | 3 | `CASIMIR_SETUP\|spin=3/2\|hbar=35/11\|J^2=Jz^2+(J+J-+J-J+)/2` | casimir_generator.py |
| `CAYLEY_HEADER` | 1 | `CAYLEY_HEADER\|0, 1, 2, 3, 4, 5, 6, 7, 8` | cayley_table_generator.py |
| `CAYLEY_ROW` | 2 | `CAYLEY_ROW\|row 0\|0, 1, 2, 3, 4, 5, 6, 7, 8` | cayley_table_generator.py |
| `CBRT` | 2 | `CBRT\|125u^6\|5u^2` | factor_special_forms_generator.py, inverse_function_generator.py, rational_exponent_generator.py |
| `CDF_EVENT` | 3 | `CDF_EVENT\|Y<=y\|X^2<=y\|X<=sqrt(y)` | rv_transform_generator.py |
| `CDF_FORMULA` | 2 | `CDF_FORMULA\|F_Y(y)=sqrt(y)/21\|0<=y<=441` | rv_transform_generator.py |
| `CEIL` | 2 | `CEIL\|4.194304\|5` | confidence_interval_generator.py |
| `CENTER` | 1, 2 | `CENTER\|(-3, -3)` | circle_equation_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, pca_generator.py |
| `CENTROID_COORD` | 3 | `CENTROID_COORD\|xbar = M_y/A\|(4913)/(867/2)\|34/3` | centroid_generator.py |
| `CENTROID_SETUP` | 3 | `CENTROID_SETUP\|0 <= y <= 3*x\|0 <= x <= 17\|centroid` | centroid_generator.py |
| `CENTROID_UPDATE` | 2 | `CENTROID_UPDATE\|C1\|(2/3,7/3)` | kmeans_step_generator.py |
| `CF_PARTIAL` | 2 | `CF_PARTIAL\|a_0\|2` | continued_fraction_generator.py |
| `CF_RESULT` | 1 | `CF_RESULT\|[2; 1, 2, 1, 4, 2, 2]` | continued_fraction_generator.py |
| `CF_SETUP` | 1 | `CF_SETUP\|282/103` | continued_fraction_generator.py |
| `CG_COEFF` | 2 | `CG_COEFF\|ket(1,-)\|0` | clebsch_gordan_generator.py |
| `CG_SETUP` | 3 | `CG_SETUP\|j1=1\|j2=1/2\|phase=-` | clebsch_gordan_generator.py |
| `CG_STATE` | 2 | `CG_STATE\|J=1/2, M=-1/2\|-sqrt(2/3)*ket(-1,+) + sqrt(1/3)*ket(0,-)` | clebsch_gordan_generator.py |
| `CHAIN` | 2 | `CHAIN\|{4, 33, 49}\|length 3` | partial_order_generator.py |
| `CHAIN_DERIV` | 2 | `CHAIN_DERIV\|dy/dx\|3/4` | activation_generator.py |
| `CHAIN_RATE` | 2 | `CHAIN_RATE\|x_s\|1` | multivar_chain_rule_generator.py |
| `CHAIN_SUM` | 3 | `CHAIN_SUM\|f_x*x_s + f_y*y_s\|3*1 + 7*(-2)\|-11` | multivar_chain_rule_generator.py |
| `CHAIN_VALUE` | 3 | `CHAIN_VALUE\|x(-1,2)\|(-1) + 2 + (-5)\|-4` | multivar_chain_rule_generator.py |
| `CHANGE_BASE` | 1 | `CHANGE_BASE\|log_25(125) = log_5(125)/log_5(25)` | log_conversion_generator.py |
| `CHAR_DIAG` | 2 | `CHAR_DIAG\|diagonal of λI - A\|(λ - 4), (λ + 1), λ` | eigenvalue_generator.py |
| `CHAR_EQ` | 2 | `CHAR_EQ\|assume y=e^(rx)\|r^2 - 6r + 9 = 0` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `CHAR_POLY` | 2 | `CHAR_POLY\|p(λ) = λ^3 - 3λ^2 - 4λ\|(λ + 1)*λ*(λ - 4)` | diagonalization_generator.py, eigenvalue_generator.py, recurrence_generator.py |
| `CHAR_ROOTS` | 2 | `CHAR_ROOTS\|r = 3\|repeated` | recurrence_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `CHAR_SETUP` | 2 | `CHAR_SETUP\|p(λ) = det(λI - A)\|triangular determinant` | eigenvalue_generator.py |
| `CHECK` | 1, 2, 3, 4 | `CHECK\|multiply_back\|23×98+45=2299\|2299` | annuity_generator.py, area_between_curves_generator.py, arithmetic_sequence_generator.py, baby_step_giant_step_generator.py, base_arithmetic_generator.py, bch_generator.py, bitwise_ops_generator.py, boolean_algebra_generator.py, cantor_diagonal_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_generator.py, cauchy_riemann_generator.py, characteristic_vector_generator.py, chi_square_generator.py, cholesky_generator.py, clebsch_gordan_generator.py, combinatory_logic_generator.py, commutator_generator.py, complement_probability_generator.py, completing_square_generator.py, conditional_probability_generator.py, convolutional_code_viterbi_generator.py, coset_generator.py, countability_bijection_generator.py, cramers_rule_generator.py, cyclic_group_generator.py, cyk_parser_generator.py, dedekind_cut_generator.py, dfa_minimization_generator.py, dfa_simulation_generator.py, diagonalization_generator.py, diffie_hellman_generator.py, ecdh_generator.py, ecdsa_generator.py, eigenvalue_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, equilibrium_ice_generator.py, error_spotting_generator.py, euler_circuit_generator.py, exact_ode_generator.py, expected_value_generator.py, experimental_probability_generator.py, extended_euclid_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, feature_map_generator.py, fill_in_step_generator.py, five_number_summary_generator.py, foundations_critic_generator.py, function_inner_product_generator.py, fundamental_counting_principle_generator.py, game_theory_generator.py, gamma_matrix_generator.py, gauss_bonnet_generator.py, gaussian_curvature_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, godel_numbering_generator.py, gradient_generator.py, gram_schmidt_generator.py, graph_counting_generator.py, hamming_code_generator.py, hereditarily_finite_set_generator.py, hermitian_check_generator.py, hessian_classify_generator.py, hilbert_axiom_derivation_generator.py, horner_evaluation_generator.py, hyperbolic_function_generator.py, hypothesis_test_generator.py, index_gymnastics_generator.py, induction_verify_generator.py, information_gain_generator.py, integers_as_pairs_generator.py, inverse_function_generator.py, kernel_perceptron_generator.py, kernel_validity_generator.py, kmeans_step_generator.py, knights_knaves_generator.py, knn_generator.py, ladder_operator_generator.py, lagrange_multiplier_generator.py, lambda_reduction_generator.py, least_squares_generator.py, legendre_construction_generator.py, lhopital_generator.py, lie_exponential_generator.py, likelihood_language_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_fractional_generator.py, lll_reduction_generator.py, log_equation_generator.py, logic_grid_puzzle_generator.py, logical_equivalence_laws_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lu_decomposition_generator.py, lz_compression_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_exponential_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, mle_generator.py, mobius_transform_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, naive_bayes_generator.py, natural_deduction_generator.py, nfa_simulation_generator.py, odds_probability_generator.py, ode_system_generator.py, operation_properties_generator.py, or_formula_generator.py, ordinal_arithmetic_generator.py, partial_derivative_generator.py, partial_order_generator.py, partial_trace_generator.py, pauli_algebra_generator.py, pca_generator.py, pda_simulation_generator.py, peano_arithmetic_generator.py, perceptron_generator.py, pollard_factorization_generator.py, polynomial_inequality_generator.py, positive_definite_generator.py, power_series_generator.py, prenex_normal_form_generator.py, prime_factorization_generator.py, probability_axioms_finite_generator.py, probability_measure_generator.py, projector_generator.py, qr_decomposition_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, quantifier_negation_generator.py, quaternion_generator.py, radical_variable_simplify_generator.py, ratio_table_generator.py, rationals_as_pairs_generator.py, recursive_explicit_generator.py, regex_to_automaton_generator.py, relation_closure_generator.py, resolution_proof_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, routh_hurwitz_generator.py, rsa_generator.py, running_coupling_generator.py, rv_transform_generator.py, sample_space_list_generator.py, semantic_tableau_generator.py, series_convergence_generator.py, set_algebra_laws_generator.py, shm_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simplex_generator.py, special_solution_equation_generator.py, statics_generator.py, stereographic_generator.py, structure_constant_generator.py, structure_isomorphism_generator.py, svd_generator.py, svm_margin_generator.py, syllogism_generator.py, systems_elimination_generator.py, taylor_series_generator.py, tip_bill_split_generator.py, tonelli_shanks_generator.py, totient_generator.py, transportation_generator.py, tree_diagram_probability_generator.py, turing_machine_trace_generator.py, two_sample_test_generator.py, two_step_equation_generator.py, type_theory_generator.py, uncertainty_generator.py, venn_region_count_generator.py, young_tableaux_generator.py, z_score_generator.py, zf_axiom_identify_generator.py |
| `CHECK_POINT` | 3 | `CHECK_POINT\|x=0\|11·0 + 18 = 18\|11·0 + 21 = 21` | special_solution_equation_generator.py |
| `CHINCHILLA` | 2 | `CHINCHILLA\|20N\|1200000000` | scaling_law_generator.py |
| `CHI_FORMULA` | 1 | `CHI_FORMULA\|E = (row·col)/N; χ² = Σ (O - E)^2/E` | chi_square_generator.py |
| `CHI_SETUP` | 2 | `CHI_SETUP\|row 1: 22, 58; row 2: 8, 12; N = 100\|independence; df = 1, critical value = 3.841` | chi_square_generator.py |
| `CHI_TERM` | 3 | `CHI_TERM\|22 - 24 = -2\|(-2)^2 = 4\|4/24 = 1/6` | chi_square_generator.py |
| `CHOLESKY_ENTRY` | 2 | `CHOLESKY_ENTRY\|l11\|4` | cholesky_generator.py |
| `CHOL_SETUP` | 2 | `CHOL_SETUP\|A = [[16, -12, -16], [-12, 13, 18], [-16, 18, 34]]\|A = L L^T` | cholesky_generator.py |
| `CHRISTOFFEL_FORMULA` | 1 | `CHRISTOFFEL_FORMULA\|Gamma^i_jk = 1/2 g^im(d_j g_mk + d_k g_mj - d_m g_jk)` | christoffel_generator.py |
| `CHRISTOFFEL_SETUP` | 3 | `CHRISTOFFEL_SETUP\|sphere\|g_phiphi=R^2, g_thetatheta=R^2 sin^2(phi)\|R=80, phi=45 deg` | christoffel_generator.py |
| `CHRISTOFFEL_VALUE` | 2 | `CHRISTOFFEL_VALUE\|Gamma^phi_thetatheta\|-2448/21025` | riemann_tensor_generator.py |
| `CHURCH_NUMERAL` | 2 | `CHURCH_NUMERAL\|2\|lambda p. (lambda k. (p (p k)))` | lambda_reduction_generator.py |
| `CIRCLE_ANGLE_SETUP` | 2 | `CIRCLE_ANGLE_SETUP\|inscribed angle 68°\|central angle on the same arc` | circle_angle_generator.py |
| `CIRCLE_CALCULATE` | 2 | `CIRCLE_CALCULATE\|C = 38π\|38π` | circle_generator.py |
| `CIRCLE_EQ` | 1 | `CIRCLE_EQ\|x^2 + (y - 4)^2 = 4` | complex_locus_generator.py |
| `CIRCLE_FORMULA` | 1 | `CIRCLE_FORMULA\|C = 2πr` | circle_generator.py |
| `CIRCLE_SETUP` | 2 | `CIRCLE_SETUP\|19\|radius` | circle_equation_generator.py, circle_generator.py |
| `CIRCLE_SUBSTITUTE` | 1 | `CIRCLE_SUBSTITUTE\|C = 2 × π × 19` | circle_generator.py |
| `CIRCULATION_SUM` | 2 | `CIRCULATION_SUM\|(-2 - 0)*15\|-30` | vector_theorem_generator.py |
| `CI_FORMULA` | 1 | `CI_FORMULA\|x̄ ± E` | confidence_interval_generator.py |
| `CI_SETUP` | 2 | `CI_SETUP\|p̂ = 0.5, n = 100, z* = 2.576\|margin of error` | confidence_interval_generator.py |
| `CLASS` | 2 | `CLASS\|digit sum 4\|{22}` | equivalence_relation_generator.py |
| `CLASSIFY` | 2 | `CLASSIFY\|contradiction\|T at 0 of 8 rows` | foundations_critic_generator.py, truth_table_generator.py |
| `CLAUSE` | 2 | `CLAUSE\|C1\|(¬P320)` | resolution_proof_generator.py |
| `CLIFFORD_EXPECT` | 3 | `CLIFFORD_EXPECT\|2*eta=0\|I_entry=1\|0` | gamma_matrix_generator.py |
| `CLOSURE_ADD` | 2 | `CLOSURE_ADD\|(24, 24)\|reflexive` | relation_closure_generator.py |
| `CLUE_APPLY` | 3 | `CLUE_APPLY\|clue 1\|Luca's item comes before Dara's item in the listed order\|24 → 12 candidates` | logic_grid_puzzle_generator.py |
| `CLUSTER_MEMBERS` | 2 | `CLUSTER_MEMBERS\|C1\|P2,P3,P4` | kmeans_step_generator.py |
| `CMP` | 2, 3 | `CMP\|44\|9\|>` | dedekind_cut_generator.py, experimental_probability_generator.py, fraction_comparison_generator.py, graph_interpret_generator.py, integers_as_pairs_generator.py, likelihood_language_generator.py, logical_connective_eval_generator.py, probability_measure_generator.py, rationals_as_pairs_generator.py, set_builder_roster_generator.py |
| `CMP_DIGIT` | 4 | `CMP_DIGIT\|pos_0\|0\|1\|<` | number_comparison_generator.py |
| `CMP_NUM` | 3 | `CMP_NUM\|46.36\|177.07\|<` | number_comparison_generator.py |
| `CNF` | 1 | `CNF\|ω^3·4 + ω^2·4 + ω·4` | ordinal_arithmetic_generator.py |
| `CNF_FORM` | 1 | `CNF_FORM\|(B OR NOT C OR NOT D) AND (NOT B OR C OR NOT D) AND (NOT B OR NOT C OR D)` | boolean_algebra_generator.py |
| `CODEWORD` | 1, 3 | `CODEWORD\|1110000` | hamming_code_generator.py, kraft_inequality_generator.py |
| `CODE_LENGTH` | 2 | `CODE_LENGTH\|A\|l=2` | huffman_coding_generator.py |
| `COEFF` | 2 | `COEFF\|a_1\|38880` | laurent_series_generator.py, series_solution_generator.py |
| `COEFFS` | 1, 2 | `COEFFS\|2, -7, 3, 3, 7` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `COEFF_MATCH` | 2 | `COEFF_MATCH\|x^n\|(n+1)a_(n+1) = 2a_n` | series_solution_generator.py |
| `COEFF_PAIR` | 3 | `COEFF_PAIR\|i=0, j=2\|0+2=2\|10` | generating_function_generator.py |
| `COFACTOR` | 2 | `COFACTOR\|(1,1) sign +\|minor [[3, -2], [2, 3]]` | determinant_generator.py |
| `COLLIDER_SETUP` | 3 | `COLLIDER_SETUP\|events_fb\|L=30 fb^-1\|sigma=18 fb` | cross_section_generator.py |
| `COLLISION` | 1 | `COLLISION\|f(k) = f(x) = 9` | function_properties_generator.py |
| `COLLISION_SETUP` | 3 | `COLLISION_SETUP\|inelastic_1d\|m1=4, u1=-2\|m2=20, u2=14` | collision_generator.py |
| `COL_BASIS` | 2 | `COL_BASIS\|original columns 1, 2\|[[-1, -2, -9], [1, 1, 3]]` | subspace_basis_generator.py |
| `COMB` | 2 | `COMB\|C(4,1)\|4` | bec_channel_generator.py |
| `COMBO` | 2 | `COMBO\|x = 17*v1 - v2\|[9, 8]` | diagonalization_generator.py |
| `COMB_CONST` | 3 | `COMB_CONST\|-1\|-6\|-7` | derivative_product_quotient_generator.py, equation_from_two_points_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMB_FORMULA` | 1 | `COMB_FORMULA\|C(n, r) = P(n, r)/r!` | permutation_combination_generator.py |
| `COMB_RULE` | 2 | `COMB_RULE\|C x y z\|x z y` | combinatory_logic_generator.py |
| `COMB_SETUP` | 2 | `COMB_SETUP\|C(9, 4)\|n!/(r!·(n-r)!)` | counting_classics_generator.py, permutation_combination_generator.py, stars_and_bars_generator.py |
| `COMB_X` | 3 | `COMB_X\|4x\|-5x\|-x` | derivative_product_quotient_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMMON_DIFF` | 2 | `COMMON_DIFF\|-5 - 4\|-9` | arithmetic_sequence_generator.py, recursive_explicit_generator.py |
| `COMMON_RATIO` | 2 | `COMMON_RATIO\|-588/(-686)\|6/7` | geometric_sequence_generator.py, recursive_explicit_generator.py |
| `COMMUTATOR` | 2 | `COMMUTATOR\|[A,B]\|[[0, -45i], [-45i, 0]]` | structure_constant_generator.py |
| `COMM_ENTRY` | 3 | `COMM_ENTRY\|(1,1)\|0 - 0\|0` | structure_constant_generator.py |
| `COMM_FORMULA` | 1 | `COMM_FORMULA\|[A,B]f=A(Bf)-B(Af)` | commutator_generator.py |
| `COMM_RESULT` | 2 | `COMM_RESULT\|[D,x]f\|x^16` | commutator_generator.py |
| `COMM_SETUP` | 3 | `COMM_SETUP\|[D,x]f\|f=x^16\|D=d/dx` | commutator_generator.py |
| `COMPARE` | 2, 3 | `COMPARE\|3 < 7\|log_b(a) < k` | algorithm_trace_generator.py, equilibrium_ice_generator.py, fixed_point_generator.py, master_theorem_generator.py |
| `COMPLEMENT` | 2, 3 | `COMPLEMENT\|P(Aᶜ) = 1 − P(A)\|1 − 4/13\|9/13` | complement_probability_generator.py, derangement_generator.py, odds_probability_generator.py, probability_axioms_finite_generator.py |
| `COMPLETE_SQUARE` | 2 | `COMPLETE_SQUARE\|half of -6 = -3\|(-3)^2 = 9` | completing_square_generator.py, conic_standard_form_generator.py, polar_parametric_generator.py |
| `COMPOSE` | 3 | `COMPOSE\|g\|f(g) = 30\|g(30) = Y` | function_properties_generator.py |
| `COMPOSE_PAIR` | 3 | `COMPOSE_PAIR\|(a, 9)\|(9, C)\|(a, C)` | relation_operations_generator.py |
| `COMPOSITE_FACTOR` | 2 | `COMPOSITE_FACTOR\|5\|73` | divisibility_classification_generator.py |
| `COMPOSITE_SETUP` | 2 | `COMPOSITE_SETUP\|area = length × width with mixed numbers\|convert, multiply, simplify` | composite_arithmetic_generator.py |
| `COMP_INEQ_PART` | 2 | `COMP_INEQ_PART\|Part 1\|5x + 4 < -4 -> x < -8/5` | compound_inequality_generator.py |
| `COMP_INEQ_SETUP` | 1 | `COMP_INEQ_SETUP\|12 < x + 10 < 18` | compound_inequality_generator.py |
| `CONCLUDE` | 1 | `CONCLUDE\|e ∣ h` | direct_proof_algebra_generator.py |
| `CONCLUSION_AT` | 2 | `CONCLUSION_AT\|r=T, s=F\|T` | argument_form_generator.py |
| `CONCLUSION_CHECK` | 1 | `CONCLUSION_CHECK\|not forced` | syllogism_generator.py |
| `COND_COUNT` | 2 | `COND_COUNT\|club=no and commute=bike\|24` | conditional_probability_generator.py |
| `COND_ENTROPY` | 1 | `COND_ENTROPY\|H(Y given X)=H(X,Y)-H(X)` | mutual_information_generator.py |
| `COND_FORMULA` | 1 | `COND_FORMULA\|P(fare=flex given route=south) = count(both)/count(route=south)` | conditional_probability_generator.py, joint_distribution_generator.py, two_way_table_probability_generator.py |
| `COND_PARTS` | 2 | `COND_PARTS\|n > 133\|n > 87` | conditional_forms_generator.py |
| `COND_SETUP` | 2 | `COND_SETUP\|yes/bike 24, no/bike 24, yes/bus 9, no/bus 9\|P(commute=bike given club=no)` | conditional_probability_generator.py |
| `COND_TOTAL` | 2 | `COND_TOTAL\|club=no total\|24 + 9 = 33` | conditional_probability_generator.py |
| `CONGRUENCE_REDUCE` | 2 | `CONGRUENCE_REDUCE\|43x congruent to 3\|mod 15` | modular_inverse_generator.py |
| `CONGRUENCE_SOLUTIONS` | 3 | `CONGRUENCE_SOLUTIONS\|base 6\|step 15\|6` | modular_inverse_generator.py |
| `CONIC_SETUP` | 2 | `CONIC_SETUP\|(y + 6)^2 = -12(x - 5)\|vertex, focus, directrix` | conic_standard_form_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `CONJ` | 2 | `CONJ\|phi_1=2-i\|2+i` | braket_generator.py |
| `CONJUGATE` | 2 | `CONJUGATE\|1 + 5i\|1 - 5i` | complex_division_generator.py, quaternion_generator.py |
| `CONNECTIVE` | 2 | `CONNECTIVE\|¬q\|T` | logical_connective_eval_generator.py |
| `CONSERVATION_SETUP` | 2 | `CONSERVATION_SETUP\|pi+ -> nu_mu + mu+ + pi0\|check=Q,B,Le,Lmu` | conservation_law_generator.py |
| `CONSERVE_CHECK` | 3 | `CONSERVE_CHECK\|Q\|left=1,right=1\|conserved` | conservation_law_generator.py |
| `CONSTRAINT_SUBST` | 3 | `CONSTRAINT_SUBST\|2*x + 5*y = 532\|lambda*(4/10 + 25/4) = 532\|lambda = 80` | lagrange_multiplier_generator.py |
| `CONST_SOLVE` | 2 | `CONST_SOLVE\|C1 = -2\|C2 = 2` | recurrence_generator.py |
| `CONTOUR_SETUP` | 3 | `CONTOUR_SETUP\|abs(z)=7\|positive orientation\|f=5/(z-7) + 6/(z+6) + 4/(z+2)` | contour_integral_generator.py |
| `CONTRADICTION` | 2 | `CONTRADICTION\|r−d is nonnegative and in S\|r−d < r` | induction_verify_generator.py |
| `CONT_DIST_SETUP` | 3 | `CONT_DIST_SETUP\|f(x)=k*x\|support=[0,13]\|interval=(1,2)` | continuous_distribution_generator.py |
| `CONVERGENT` | 2 | `CONVERGENT\|i=0\|2/1` | continued_fraction_generator.py |
| `CONVERGE_CHECK` | 2 | `CONVERGE_CHECK\|abs(r) = 6/7 < 1\|converges` | geometric_sequence_generator.py, series_convergence_generator.py |
| `CONV_ENCODE_STEP` | 3 | `CONV_ENCODE_STEP\|i=1\|prev=0,u=0\|00` | convolutional_code_viterbi_generator.py |
| `CONV_FACTOR` | 2 | `CONV_FACTOR\|1 hr\|60 min` | cross_section_generator.py, dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, unit_conversion_generator.py |
| `CONV_INIT` | 2 | `CONV_INIT\|h_-2=0,h_-1=1\|k_-2=1,k_-1=0` | continued_fraction_generator.py |
| `CONV_RECEIVED` | 2 | `CONV_RECEIVED\|101101\|flipped position 1` | convolutional_code_viterbi_generator.py |
| `CONV_RESULT` | 2 | `CONV_RESULT\|41 hr\|2460 min` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, temperature_conversion_generator.py, unit_conversion_generator.py |
| `CONV_SETUP` | 2, 3 | `CONV_SETUP\|x=[0,5,7]\|h=[8,3,8]` | convolution_generator.py, convolutional_code_viterbi_generator.py |
| `CONV_STEP` | 3 | `CONV_STEP\|i=0\|h=2\|k=1` | continued_fraction_generator.py |
| `CONV_SUM` | 2 | `CONV_SUM\|n=0\|0` | convolution_generator.py |
| `CONV_WINDOW` | 2 | `CONV_WINDOW\|n=0\|x0*h0` | convolution_generator.py |
| `COORDS` | 2 | `COORDS\|c = P^-1 x\|[17, -1]` | diagonalization_generator.py |
| `CORRECT_BIT` | 3 | `CORRECT_BIT\|position=4\|0->1\|corrected=1011010` | hamming_code_generator.py |
| `CORR_FORMULA` | 1 | `CORR_FORMULA\|r = Sxy/√(Sxx·Syy)` | joint_distribution_generator.py, regression_generator.py |
| `COS` | 2 | `COS\|3pi/2\|0` | positional_encoding_generator.py |
| `COSET` | 2 | `COSET\|1H\|{1, 19, 9, 39, 37, 43, 25, 35, 5, 7}` | coset_generator.py |
| `COSET_ELEM` | 2 | `COSET_ELEM\|1H\|1` | coset_generator.py |
| `COSET_SKIP` | 2 | `COSET_SKIP\|5\|already listed` | coset_generator.py |
| `COSET_START` | 2 | `COSET_START\|rep 1\|1H` | coset_generator.py |
| `COSINE` | 2 | `COSINE\|A,A\|1` | embedding_similarity_generator.py, lr_schedule_generator.py |
| `COST` | 1 | `COST\|initial` | transportation_generator.py |
| `COUNT` | 2 | `COUNT\|neither\|5` | attribute_sorting_generator.py, bayesian_update_generator.py, equivalence_relation_generator.py, likelihood_language_generator.py, logical_connective_eval_generator.py, method_of_moments_generator.py, mle_generator.py, one_to_one_correspondence_generator.py, probability_addition_rule_generator.py, random_digit_simulation_generator.py, set_builder_roster_generator.py, set_membership_subset_generator.py, set_operations_generator.py |
| `COUNTEREXAMPLE` | 2, 3 | `COUNTEREXAMPLE\|set pair\|A = ∅; B = {77}; left = ∅; right = {77}` | argument_form_generator.py, conditional_forms_generator.py, counterexample_search_generator.py, truth_table_generator.py |
| `COUNTERMODEL` | 1 | `COUNTERMODEL\|farmers=TFF, artists=FTF, bakers=FTF` | syllogism_generator.py |
| `COUNT_DP` | 3 | `COUNT_DP\|1\|1\|2` | decimal_mult_generator.py |
| `COUNT_RULE` | 2 | `COUNT_RULE\|k-subsets\|C(n,k) = n(n−1)…(n−k+1)/k!` | function_properties_generator.py, set_counting_generator.py |
| `COUNT_SETUP` | 1, 2 | `COUNT_SETUP\|arrangements of 7 cards\|7!` | counting_classics_generator.py, counting_to_probability_generator.py |
| `COUPON` | 1 | `COUPON\|612` | bond_pricing_generator.py |
| `COVER` | 3 | `COVER\|2\|27\|no c strictly between` | partial_order_generator.py |
| `COV_ENTRY` | 2 | `COV_ENTRY\|xx\|32` | pca_generator.py |
| `COV_FORMULA` | 1 | `COV_FORMULA\|Cov=E[XY]-E[X]E[Y]` | joint_distribution_generator.py |
| `CRC_CHECK` | 3 | `CRC_CHECK\|codeword=110110000001\|remainder=000\|valid` | crc_generator.py |
| `CRC_REMAINDER` | 1 | `CRC_REMAINDER\|001` | crc_generator.py |
| `CRC_SETUP` | 3 | `CRC_SETUP\|data=110110000\|poly=1101\|augmented=110110000000` | crc_generator.py |
| `CRC_SKIP` | 2 | `CRC_SKIP\|i=1\|leading bit 0` | crc_generator.py |
| `CRC_XOR` | 3 | `CRC_XOR\|i=0\|1101 xor 1101\|0000` | crc_generator.py |
| `CRIT_EQS` | 2 | `CRIT_EQS\|f_x = 0\|-4*x - 3*y = 0` | hessian_classify_generator.py |
| `CRIT_SOLVE` | 3 | `CRIT_SOLVE\|det\|(-4)*(-8) - (-3)^2\|23` | hessian_classify_generator.py |
| `CROSS_ENTROPY` | 2 | `CROSS_ENTROPY\|target=3\|ln(3)` | perplexity_generator.py, softmax_gradient_generator.py |
| `CROSS_MULT` | 1 | `CROSS_MULT\|16·EF = 32·12` | similar_triangles_generator.py, triangle_solve_generator.py |
| `CROSS_RATIO` | 1 | `CROSS_RATIO\|-7/2` | mobius_transform_generator.py |
| `CROSS_RATIO_SETUP` | 4 | `CROSS_RATIO_SETUP\|z1=6\|z2=-6\|z3=2\|z4=8` | mobius_transform_generator.py |
| `CRT_CHECK` | 3 | `CRT_CHECK\|i=1\|5\|5` | crt_generator.py |
| `CRT_CONGRUENCE` | 3 | `CRT_CONGRUENCE\|i=1\|x=5\|mod 9` | crt_generator.py |
| `CRT_FACTOR` | 3 | `CRT_FACTOR\|i=1\|M_i=11\|mod 9` | crt_generator.py |
| `CRT_SETUP` | 1 | `CRT_SETUP\|2 congruences` | crt_generator.py |
| `CRT_TERM` | 2 | `CRT_TERM\|i=1\|275` | crt_generator.py |
| `CRT_TOTAL_MODULUS` | 2 | `CRT_TOTAL_MODULUS\|9, 11\|99` | crt_generator.py |
| `CR_SETUP` | 2 | `CR_SETUP\|u=-x^2 + y^2 + 5x + y\|v=-2xy - x + 5y` | cauchy_riemann_generator.py |
| `CUM_INTERVAL` | 2 | `CUM_INTERVAL\|A\|[0,1/2)` | arithmetic_coding_generator.py |
| `CURL_COMPONENT` | 3 | `CURL_COMPONENT\|Q_x - P_y\|2 - 4\|-2` | div_curl_generator.py |
| `CURRENT_YIELD` | 1 | `CURRENT_YIELD\|15/112` | bond_pricing_generator.py |
| `CURVATURE_FORMULA` | 2 | `CURVATURE_FORMULA\|circle\|kappa = 1/R` | curve_geometry_generator.py |
| `CURVE_GEOM_SETUP` | 3 | `CURVE_GEOM_SETUP\|r(t) = <5*t + 7, 12*t + 4>\|0 <= t <= 10\|arc length` | curve_geometry_generator.py |
| `CURVE_SETUP` | 2 | `CURVE_SETUP\|f(x) = x^3 - 12x^2 + 36x + 6\|inflection point and concavity` | curve_analysis_generator.py |
| `CUT_RULE` | 2 | `CUT_RULE\|L(√2)\|q < 0 or q² < 2` | dedekind_cut_generator.py |
| `CW_START` | 2 | `CW_START\|leading 1\|1/1` | countability_bijection_generator.py |
| `CW_STEP` | 3 | `CW_STEP\|bit 0\|1/1\|1/2` | countability_bijection_generator.py |
| `CX_A` | 3 | `CX_A\|3/5\|0\|3/5` | braket_generator.py, spin_half_generator.py |
| `CX_M` | 3 | `CX_M\|1\|3/5\|3/5` | braket_generator.py, spin_half_generator.py |
| `CX_SETUP` | 2 | `CX_SETUP\|(-8 + 2i) - (8 - 8i)\|subtract` | complex_division_generator.py, complex_number_ops_generator.py |
| `CYCLE` | 1 | `CYCLE\|(1 2 4)` | permutation_group_generator.py |
| `CYCLE_LENGTHS` | 1 | `CYCLE_LENGTHS\|3, 2` | permutation_group_generator.py |
| `CYCLE_REJECT` | 2 | `CYCLE_REJECT\|AC\|endpoints already connected` | mst_generator.py |
| `CYCLE_TRACE` | 2 | `CYCLE_TRACE\|start 1\|1->2->4->1` | permutation_group_generator.py |
| `CYCLIC_START` | 2 | `CYCLIC_START\|3\|identity 1` | cyclic_group_generator.py |
| `CYCLIC_SUBGROUP` | 2 | `CYCLIC_SUBGROUP\|{1, 3}\|2` | cyclic_group_generator.py |
| `CYK_CELL` | 2 | `CYK_CELL\|1,2\|{}` | cyk_parser_generator.py |
| `CYK_COMBINE` | 3 | `CYK_COMBINE\|E Z\|{Z}\|cell 2,3` | cyk_parser_generator.py |
| `CYK_RULE` | 2 | `CYK_RULE\|E\|a or E E` | cyk_parser_generator.py |
| `CYK_SETUP` | 2 | `CYK_SETUP\|string dad\|length 3` | cyk_parser_generator.py |
| `CYK_SPAN` | 1 | `CYK_SPAN\|2` | cyk_parser_generator.py |
| `CYK_SPLIT` | 3 | `CYK_SPLIT\|cell 1,2\|1,1 x 2,2\|{V,Z} x {E}` | cyk_parser_generator.py |
| `CYK_TERMINAL` | 3 | `CYK_TERMINAL\|cell 1,1\|d\|{V,Z}` | cyk_parser_generator.py |
| `CYL_BOUNDS` | 2 | `CYL_BOUNDS\|z\|0..10` | triple_integral_generator.py |
| `CYL_CONVERT` | 2 | `CYL_CONVERT\|4*z dV\|4*z*r dz dr dtheta` | triple_integral_generator.py |
| `D` | 3 | `D\|632\|99\|6` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, annuity_generator.py, antiderivative_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, bayesian_update_generator.py, bisection_generator.py, blackbody_generator.py, bond_pricing_generator.py, branching_ratio_generator.py, cantor_pairing_generator.py, casimir_force_generator.py, cholesky_generator.py, christoffel_generator.py, circle_angle_generator.py, circle_equation_generator.py, classifier_metrics_generator.py, collision_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continuous_distribution_generator.py, coset_generator.py, countability_bijection_generator.py, counting_classics_generator.py, cramers_rule_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, de_moivre_generator.py, decimal_div_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, dimensional_analysis_generator.py, doppler_generator.py, einstein_summation_generator.py, electrostatics_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, equilibrium_ice_generator.py, error_spotting_generator.py, exact_ode_generator.py, exponential_equation_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finite_difference_generator.py, flops_memory_generator.py, fourier_series_generator.py, function_inner_product_generator.py, function_operations_generator.py, game_theory_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, hamiltonian_generator.py, hawking_generator.py, heat_engine_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypothesis_test_generator.py, information_gain_generator.py, integrating_factor_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, jacobi_symbol_generator.py, joint_distribution_generator.py, kernel_ridge_generator.py, kinematics_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, least_squares_generator.py, legendre_construction_generator.py, limit_evaluation_generator.py, linear_simple_generator.py, log_conversion_generator.py, logistic_growth_generator.py, long_division_generator.py, lr_schedule_generator.py, magnetism_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_inverse_generator.py, matrix_norm_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, midpoint_generator.py, mle_generator.py, modular_inverse_generator.py, multi_step_unit_conversion_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, npv_irr_generator.py, ode_substitution_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, param_count_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, partition_function_generator.py, pca_generator.py, percent_problem_generator.py, permutation_combination_generator.py, perplexity_generator.py, physics_formula_generator.py, planck_units_generator.py, polar_parametric_generator.py, primality_test_generator.py, probability_measure_generator.py, projectile_motion_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, recurrence_generator.py, regression_generator.py, regular_polygon_area_generator.py, relativistic_energy_generator.py, repeating_decimal_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_counting_generator.py, shm_generator.py, similar_triangles_generator.py, simplex_generator.py, sinusoid_features_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, standard_deviation_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, stoichiometry_generator.py, svm_margin_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, totient_generator.py, transient_circuit_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, u_substitution_generator.py, undetermined_coeff_generator.py, unit_conversion_generator.py, variation_parameters_generator.py, vector_ops_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `DALEMBERT` | 1 | `DALEMBERT\|u=(f(x-ct)+f(x+ct))/2` | separable_pde_generator.py |
| `DATA_PRECISION` | 1 | `DATA_PRECISION\|n/sigma^2` | bayesian_update_generator.py |
| `DATE_ORDINAL` | 2 | `DATE_ORDINAL\|2024-05-07\|739013` | calendar_arithmetic_generator.py |
| `DB_FORMULA` | 1 | `DB_FORMULA\|G_dB=10*log10(P2/P1)` | signal_arithmetic_generator.py |
| `DECISION` | 2 | `DECISION\|f(x)\|-61` | kernel_perceptron_generator.py, svm_margin_generator.py |
| `DECODE` | 2 | `DECODE\|111110111\|{a, c, e, l, p, t, u, x}` | characteristic_vector_generator.py |
| `DEC_ADD_COL` | 3 | `DEC_ADD_COL\|frac_0\|0+1+0\|->1 (carry 0)` | decimal_add_sub_generator.py |
| `DEC_ALIGN` | 2 | `DEC_ALIGN\|55.60\|69.81` | decimal_add_sub_generator.py |
| `DEC_CARRY_FINAL` | 1 | `DEC_CARRY_FINAL\|1` | decimal_add_sub_generator.py |
| `DEC_SHIFT` | 3 | `DEC_SHIFT\|33.0/0.2\|330/2\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `DEC_SUB_COL` | 3 | `DEC_SUB_COL\|frac_0\|1-0 (borrow_in 0)\|->1 (borrow_out 0)` | decimal_add_sub_generator.py |
| `DEC_TO_FRAC` | 2 | `DEC_TO_FRAC\|4.17\|417/100` | fraction_decimal_percent_converter.py |
| `DEC_TO_PERCENT` | 2 | `DEC_TO_PERCENT\|1.075\|107.5%` | fraction_decimal_percent_converter.py, percent_problem_generator.py, simple_probability_generator.py, tip_bill_split_generator.py |
| `DEC_TYPE` | 2 | `DEC_TYPE\|151/228\|repeating` | repeating_decimal_generator.py |
| `DEC_VALUE` | 2 | `DEC_VALUE\|151/228\|0.66(228070175438596491)` | repeating_decimal_generator.py |
| `DEDUCE` | 3 | `DEDUCE\|Dara\|item = ticket\|only solution left` | logic_grid_puzzle_generator.py |
| `DEDUP` | 2 | `DEDUP\|A raw [24, 57, 66, 52, 63, 66]\|{24, 52, 57, 63, 66}` | set_membership_subset_generator.py |
| `DEGREE` | 2, 3 | `DEGREE\|A\|C, E\|2` | euler_circuit_generator.py, graph_counting_generator.py |
| `DEGREE_COMPARE` | 2 | `DEGREE_COMPARE\|deg num = deg den = 2\|y = 5/2` | limit_evaluation_generator.py, rational_function_features_generator.py, series_convergence_generator.py |
| `DEGREE_SEQUENCE` | 1 | `DEGREE_SEQUENCE\|4, 3, 2, 2, 1` | graph_counting_generator.py |
| `DELTA_VALUE` | 2 | `DELTA_VALUE\|delta_22\|1` | index_gymnastics_generator.py |
| `DEMOIVRE_POWER` | 1 | `DEMOIVRE_POWER\|16 cis(240 deg)` | de_moivre_generator.py |
| `DEMOIVRE_SETUP` | 2, 4 | `DEMOIVRE_SETUP\|power\|r=2\|theta=330 deg\|n=4` | de_moivre_generator.py |
| `DENSITY` | 2 | `DENSITY\|f_XY(x,y)\|1/22^2` | rv_transform_generator.py |
| `DENSITY_MATRIX` | 1 | `DENSITY_MATRIX\|rho=[[2/7,0],[0,5/7]]` | density_matrix_generator.py |
| `DENSITY_SETUP` | 2, 3 | `DENSITY_SETUP\|state=Phi_phase\|psi=(ket00 + e^(i143π/90)ket11)/sqrt(2)` | density_matrix_generator.py, partial_trace_generator.py |
| `DEPTH` | 1, 2 | `DEPTH\|3` | wff_parsing_generator.py |
| `DEQUANT_VALUE` | 2 | `DEQUANT_VALUE\|1\|3/2` | quantization_generator.py |
| `DERANGE_PROB` | 2 | `DERANGE_PROB\|D_6/6!\|265/720` | derangement_generator.py |
| `DERANGE_SETUP` | 2 | `DERANGE_SETUP\|n = 6\|no item fixed` | derangement_generator.py |
| `DERANGE_VALUE` | 2 | `DERANGE_VALUE\|D_2\|1` | derangement_generator.py |
| `DERIV` | 2, 3 | `DERIV\|d_phi g_thetatheta\|2R^2 sin(phi)cos(phi)` | christoffel_generator.py, gaussian_curvature_generator.py, riemann_tensor_generator.py |
| `DERIVATIVE` | 1, 2 | `DERIVATIVE\|g'(x)\|1/9` | fixed_point_generator.py, mgf_generator.py, mle_generator.py |
| `DERIVED` | 2 | `DERIVED\|C5\|(P14166)` | resolution_proof_generator.py |
| `DERIV_FORM` | 2 | `DERIV_FORM\|y'\|(C2 + 3(C1 + C2x))e^(3x)` | second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `DERIV_RULE` | 2 | `DERIV_RULE\|power rule\|d/dx of c·x^n = c·n·x^(n-1)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, multivar_chain_rule_generator.py |
| `DERIV_SERIES` | 2 | `DERIV_SERIES\|y'\|sum (n+1)a_(n+1)x^n` | series_solution_generator.py |
| `DERIV_SETUP` | 2 | `DERIV_SETUP\|f(x) = -7x^2 - 6x - x^(-3)\|f'(x)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, log_diff_higher_order_generator.py, tangent_line_generator.py |
| `DESIGN_MATRIX` | 2 | `DESIGN_MATRIX\|X = [[1, -3], [1, -1], [1, 1], [1, 3]]\|y = [8, 10, 6, -4]` | least_squares_generator.py |
| `DET` | 2 | `DET\|K\|-64` | kernel_ridge_generator.py, kernel_validity_generator.py |
| `DET2` | 2 | `DET2\|ad - bc\|-12` | ode_system_generator.py |
| `DET_FORMULA` | 1 | `DET_FORMULA\|det = ad - bc` | cramers_rule_generator.py, determinant_generator.py, matrix_inverse_generator.py |
| `DEV_ROW` | 3 | `DEV_ROW\|25\|1\|1` | standard_deviation_generator.py |
| `DFA_ACCEPT` | 1 | `DFA_ACCEPT\|q2` | dfa_minimization_generator.py, dfa_simulation_generator.py |
| `DFA_INPUT` | 1 | `DFA_INPUT\|1111` | dfa_simulation_generator.py |
| `DFA_MIN_SETUP` | 3 | `DFA_MIN_SETUP\|states A, B, C\|alphabet 0, 1\|start A` | dfa_minimization_generator.py |
| `DFA_MIN_TRANSITION` | 3 | `DFA_MIN_TRANSITION\|A\|0\|A` | dfa_minimization_generator.py |
| `DFA_READ` | 2 | `DFA_READ\|pos 1\|1` | dfa_simulation_generator.py |
| `DFA_SETUP` | 3 | `DFA_SETUP\|states q0, q1, q2\|alphabet 0, 1\|start q0` | dfa_simulation_generator.py |
| `DFA_STATE` | 2 | `DFA_STATE\|start\|q0` | dfa_simulation_generator.py |
| `DFA_STEP` | 3 | `DFA_STEP\|q0\|1\|q1` | dfa_simulation_generator.py |
| `DFA_TRANSITION` | 3 | `DFA_TRANSITION\|q0\|0\|q0` | dfa_simulation_generator.py |
| `DFS_EDGE` | 2 | `DFS_EDGE\|B->A\|tree` | graph_traversal_generator.py |
| `DFT_BIN` | 1 | `DFT_BIN\|X0=x0+x1+x2+x3` | dft_generator.py |
| `DFT_SETUP` | 2 | `DFT_SETUP\|N=4\|x=[9,9,1,8]` | dft_generator.py |
| `DH_PUBLIC` | 2 | `DH_PUBLIC\|Alice\|4` | diffie_hellman_generator.py |
| `DH_SECRET` | 2 | `DH_SECRET\|Alice\|10` | diffie_hellman_generator.py |
| `DH_SETUP` | 2 | `DH_SETUP\|p=19\|g=15` | diffie_hellman_generator.py |
| `DH_SHARED` | 2 | `DH_SHARED\|Alice\|11` | diffie_hellman_generator.py |
| `DIAG` | 2 | `DIAG\|row 1\|1` | cantor_diagonal_generator.py |
| `DIAGONAL` | 3 | `DIAGONAL\|w=191\|start=18336\|offset=81` | cantor_pairing_generator.py |
| `DIAG_FORM` | 3 | `DIAG_FORM\|P = [[1, 8], [1, 9]]\|D = [[2, 0], [0, 5]]\|P^-1 = [[9, -8], [-1, 1]]` | diagonalization_generator.py, matrix_exponential_generator.py |
| `DIFF_ROW` | 2 | `DIFF_ROW\|Delta y\|[-4, 20, 44]` | finite_difference_generator.py |
| `DIFF_SETUP` | 3 | `DIFF_SETUP\|f(x,y) = 4*x^2 + 2*y^2 + 4*x*y - 3*x\|point (-3, 3)\|dx=-1/2, dy=2/5` | multivar_chain_rule_generator.py |
| `DIFF_SUM` | 3 | `DIFF_SUM\|f_x*dx + f_y*dy\|(-15)*(-1/2) + 0*2/5\|7.5` | multivar_chain_rule_generator.py |
| `DIGIT_MAP` | 2 | `DIGIT_MAP\|success\|0–0 (1 of 10 digits)` | random_digit_simulation_generator.py |
| `DIGIT_SCAN` | 3 | `DIGIT_SCAN\|299\|makes 0\|no` | random_digit_simulation_generator.py |
| `DIJKSTRA_INIT` | 2 | `DIJKSTRA_INIT\|start E\|A=inf, B=inf, C=inf, D=inf, E=0` | dijkstra_generator.py |
| `DIM` | 2 | `DIM\|2*5+1\|11` | casimir_generator.py |
| `DIRECTRIX` | 1 | `DIRECTRIX\|x = 8` | parabola_features_generator.py |
| `DISC` | 2, 3 | `DISC\|6400\|-153600\|160000` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `DISC_CLASSIFY` | 2 | `DISC_CLASSIFY\|20 > 0\|two real solutions` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py |
| `DIST` | 3 | `DIST\|-3\|5x-1\|-15x+3` | derivative_limit_def_generator.py, derivative_product_quotient_generator.py, equation_from_two_points_generator.py, function_composition_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, polar_parametric_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, simplify_expression_generator.py, solid_revolution_generator.py, special_solution_equation_generator.py, tangent_line_generator.py |
| `DIST2` | 2, 3 | `DIST2\|P1\|C1\|41` | embedding_similarity_generator.py, kernel_evaluation_generator.py, kmeans_step_generator.py |
| `DIST_COMBINE` | 1 | `DIST_COMBINE\|-18x + 8 = 8` | systems_substitution_generator.py |
| `DIST_FORMULA` | 1 | `DIST_FORMULA\|d = √((x2 - x1)^2 + (y2 - y1)^2)` | complex_locus_generator.py, distance_formula_generator.py, hypercube_counting_generator.py |
| `DIST_SETUP` | 3 | `DIST_SETUP\|uniform\|[-5,2]\|interval=(-4,-3)` | named_distribution_generator.py |
| `DIST_TABLE` | 2 | `DIST_TABLE\|visited E\|A=9, B=inf, C=inf, D=4, E=0` | dijkstra_generator.py |
| `DIST_TERM` | 2 | `DIST_TERM\|2x\|- 4x^3 - 6x^2 - 6x` | multiplying_polynomials_generator.py |
| `DIVIDE_EQ` | 2 | `DIVIDE_EQ\|divide by y^2\|y^(-2)dy/dx + y^(-1) = 3` | ode_substitution_generator.py |
| `DIVMOD` | 3, 4 | `DIVMOD\|248\|2\|124\|r=0` | base_conversion_generator.py, induction_verify_generator.py, recursive_definition_unfold_generator.py |
| `DIV_CHECK` | 3 | `DIV_CHECK\|6\|2\|remainder 0` | conditional_forms_generator.py, counterexample_search_generator.py, divisibility_classification_generator.py, logical_connective_eval_generator.py, set_builder_roster_generator.py |
| `DIV_COEFF` | 3 | `DIV_COEFF\|-7\|-1\|x=7` | linear_complex_generator.py |
| `DIV_SETUP` | 2 | `DIV_SETUP\|330\|2` | decimal_div_generator.py, percent_problem_generator.py |
| `DIV_SUM` | 3 | `DIV_SUM\|P_x + Q_y\|-4 - 3\|-7` | div_curl_generator.py |
| `DIV_TERM` | 3 | `DIV_TERM\|12x^3\|6\|2x^3` | factor_gcf_generator.py, finite_field_generator.py, polynomial_long_division_generator.py |
| `DNF_FORM` | 1 | `DNF_FORM\|(NOT J AND NOT K AND NOT L AND M) OR (NOT J AND NOT K AND L AND NOT M) OR (J AND NOT K AND NOT L AND M) OR (J AND NOT K AND L AND M) OR (J AND K AND L AND NOT M)` | boolean_algebra_generator.py |
| `DOMAIN` | 1, 2 | `DOMAIN\|x = −22..−7\|{−22, −21, −20, −19, −18, −17, −16, −15, −14, −13, −12, −11, −10, −9, −8, −7}` | quantifier_finite_domain_generator.py, relation_operations_generator.py, set_builder_roster_generator.py |
| `DOMAIN_COND` | 2 | `DOMAIN_COND\|denominator ≠ 0\|x - 3 ≠ 0` | domain_range_generator.py |
| `DOMAIN_NOTE` | 2 | `DOMAIN_NOTE\|x ≠ 6\|denominator cannot be zero` | domain_range_generator.py, log_equation_generator.py, logistic_growth_generator.py, probability_addition_rule_generator.py, rational_equation_generator.py, unit_circle_generator.py |
| `DOPPLER_FORMULA` | 1 | `DOPPLER_FORMULA\|f_obs=f*sqrt((1+beta)/(1-beta))` | doppler_generator.py |
| `DOPPLER_SETUP` | 3 | `DOPPLER_SETUP\|relativistic_approach\|f=756\|beta=40/41` | doppler_generator.py |
| `DOT` | 2, 3 | `DOT\|(14, -11) · (-3/5, 4/5)\|14*(-3/5) + (-11)*4/5\|-17.2` | embedding_similarity_generator.py, feature_map_generator.py, fundamental_form_generator.py, gradient_generator.py, gram_schmidt_generator.py, kernel_evaluation_generator.py, line_integral_generator.py, lll_reduction_generator.py, qr_decomposition_generator.py |
| `DOT4` | 4 | `DOT4\|gamma0gamma0\|(1,1)\|1*1 + 0*0 + 0*0 + 0*0\|1` | gamma_matrix_generator.py |
| `DOT_FORMULA` | 1 | `DOT_FORMULA\|u ⊥ v exactly when u·v = 0` | dot_product_generator.py |
| `DOUBLE_SETUP` | 2, 3 | `DOUBLE_SETUP\|integrand x^2 + y^2\|upper-half disk radius 2` | double_integral_generator.py |
| `DPLL_BACKTRACK` | 2 | `DPLL_BACKTRACK\|A\|True` | dpll_trace_generator.py |
| `DPLL_BRANCH` | 3 | `DPLL_BRANCH\|depth 0\|A\|True` | dpll_trace_generator.py |
| `DPLL_CONFLICT` | 1 | `DPLL_CONFLICT\|A=True, B=True` | dpll_trace_generator.py |
| `DPLL_SAT` | 1 | `DPLL_SAT\|A=True, B=True, C=True` | dpll_trace_generator.py |
| `DPLL_SETUP` | 3 | `DPLL_SETUP\|(A) AND (not A OR B) AND (not B OR C)\|variables A, B, C\|True first` | dpll_trace_generator.py |
| `DPLL_SIMPLIFY` | 2 | `DPLL_SIMPLIFY\|A=True\|2 clauses left` | dpll_trace_generator.py |
| `DPLL_STATE` | 3 | `DPLL_STATE\|depth 0\|none\|3 clauses left` | dpll_trace_generator.py |
| `DPLL_UNIT` | 2 | `DPLL_UNIT\|(A)\|A=True` | dpll_trace_generator.py |
| `DP_CELL` | 3 | `DP_CELL\|i=1,j=0\|delete 1 chars\|1` | dp_table_generator.py |
| `DP_COINS` | 1 | `DP_COINS\|1, 3, 4` | dp_table_generator.py |
| `DP_ITEMS` | 1 | `DP_ITEMS\|1:(w=3,v=6); 2:(w=1,v=2); 3:(w=1,v=9); 4:(w=5,v=5)` | dp_table_generator.py |
| `DP_ROW` | 2 | `DP_ROW\|i=0\|0, 1, 2, 3, 4, 5` | dp_table_generator.py |
| `DP_SETUP` | 2, 3 | `DP_SETUP\|edit distance\|source=DDD\|target=DABBA` | dp_table_generator.py |
| `D_POWER` | 2 | `D_POWER\|D^3\|[[1, 0], [0, 27]]` | diagonalization_generator.py |
| `E` | 3 | `E\|9\|2\|81` | ac_circuit_generator.py, adam_step_generator.py, angle_defect_generator.py, annuity_generator.py, arc_sector_generator.py, backprop_generator.py, bec_channel_generator.py, blackbody_generator.py, bond_pricing_generator.py, casimir_force_generator.py, casimir_generator.py, christoffel_generator.py, circle_equation_generator.py, complex_division_generator.py, complex_locus_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continuous_distribution_generator.py, counting_to_probability_generator.py, de_moivre_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, density_matrix_generator.py, derivative_limit_def_generator.py, diagonalization_generator.py, distance_formula_generator.py, doppler_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, euler_formula_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, feature_map_generator.py, finance_generator.py, four_vector_generator.py, fractal_iteration_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, fundamental_form_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, gradient_descent_generator.py, gradient_step_generator.py, hamiltonian_generator.py, hawking_generator.py, hermitian_check_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, invariant_mass_generator.py, kernel_evaluation_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, lagrangian_generator.py, laurent_series_generator.py, layer_norm_generator.py, limit_evaluation_generator.py, log_conversion_generator.py, log_equation_generator.py, log_properties_generator.py, low_rank_approx_generator.py, matrix_group_check_generator.py, matrix_norm_generator.py, mean_value_theorem_generator.py, metric_arc_length_generator.py, mgf_generator.py, minkowski_interval_generator.py, mobius_transform_generator.py, named_distribution_generator.py, natural_units_generator.py, npv_irr_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_statistics_generator.py, particle_in_box_generator.py, pca_generator.py, piecewise_evaluation_generator.py, planck_units_generator.py, polar_parametric_generator.py, portfolio_generator.py, projectile_motion_generator.py, pythag_hyp_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, rv_transform_generator.py, schwarzschild_generator.py, set_counting_generator.py, set_operations_generator.py, shm_generator.py, spherical_excess_generator.py, spin_half_generator.py, stereographic_generator.py, svm_margin_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, uncertainty_generator.py, vector_ops_generator.py, wavefunction_generator.py, z_transform_generator.py |
| `ECDH_SETUP` | 2 | `ECDH_SETUP\|E:y^2=x^3+2x+2 over F_17\|G=(5,1)` | ecdh_generator.py |
| `ECDSA_NONCE` | 2 | `ECDSA_NONCE\|kG=(16,4)\|r=16` | ecdsa_generator.py |
| `ECDSA_PUBLIC` | 1 | `ECDSA_PUBLIC\|Q=dG=(0,6)` | ecdsa_generator.py |
| `ECDSA_SETUP` | 4 | `ECDSA_SETUP\|E/F_17, G=(5,1), n=19\|d=7\|z=5\|k=13` | ecdsa_generator.py |
| `ECDSA_SIGN` | 2 | `ECDSA_SIGN\|s=k^-1(z+rd) mod n\|s=9` | ecdsa_generator.py |
| `ECDSA_VERIFY` | 2 | `ECDSA_VERIFY\|u1=9\|u2=6` | ecdsa_generator.py |
| `EC_ACCUM` | 2 | `EC_ACCUM\|1P\|(1,12)` | elliptic_curve_finite_field_generator.py |
| `EC_ADD` | 1 | `EC_ADD\|(16,4)` | ecdsa_generator.py |
| `EC_IDENTITY` | 2 | `EC_IDENTITY\|O + Q\|(1,12)` | elliptic_curve_finite_field_generator.py |
| `EC_INVERSE` | 3 | `EC_INVERSE\|(2,7)\|(2,12)\|O` | elliptic_curve_finite_field_generator.py |
| `EC_POINT_CHECK` | 3 | `EC_POINT_CHECK\|P\|O\|identity` | elliptic_curve_finite_field_generator.py |
| `EC_PUBLIC` | 2 | `EC_PUBLIC\|A=(16,13)\|B=(0,6)` | ecdh_generator.py |
| `EC_SCALAR` | 2 | `EC_SCALAR\|a=6\|aG=(16,13)` | ecdh_generator.py, ecdsa_generator.py |
| `EC_SCALAR_SETUP` | 2 | `EC_SCALAR_SETUP\|k=5\|P=(1,12)` | elliptic_curve_finite_field_generator.py |
| `EC_SETUP` | 3 | `EC_SETUP\|p=23\|a=1\|b=4` | elliptic_curve_finite_field_generator.py |
| `EC_SHARED` | 2 | `EC_SHARED\|aB=(3,1)\|bA=(3,1)` | ecdh_generator.py |
| `EC_SLOPE` | 2 | `EC_SLOPE\|2P\|4` | elliptic_curve_finite_field_generator.py |
| `EC_SLOPE_FORMULA` | 2 | `EC_SLOPE_FORMULA\|2P\|(3x1^2+a)/(2y1)` | elliptic_curve_finite_field_generator.py |
| `EC_X3` | 2 | `EC_X3\|2P\|14` | elliptic_curve_finite_field_generator.py |
| `EC_Y3` | 2 | `EC_Y3\|2P\|5` | elliptic_curve_finite_field_generator.py |
| `EDGE_CHECK` | 3 | `EDGE_CHECK\|(1117, 1117)\|(p, p)\|present` | structure_isomorphism_generator.py |
| `EDGE_CHOOSE` | 3 | `EDGE_CHOOSE\|AE\|weight 2\|add E` | mst_generator.py |
| `EDGE_CONSIDER` | 2 | `EDGE_CONSIDER\|AB\|weight 3` | mst_generator.py |
| `EDGE_COUNT` | 2 | `EDGE_COUNT\|m\|6` | euler_circuit_generator.py, graph_counting_generator.py |
| `EDGE_LIST` | 1 | `EDGE_LIST\|AB, AE, BC, CD, CE, DE` | euler_circuit_generator.py |
| `EDGE_WEIGHT` | 2 | `EDGE_WEIGHT\|AB\|1` | dijkstra_generator.py, mst_generator.py |
| `EIGENPAIR` | 2 | `EIGENPAIR\|lambda = -3\|[1, 1]` | ode_system_generator.py |
| `EIGENVALUE` | 1, 2 | `EIGENVALUE\|λ = -1\|p(-1) = 0` | diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, separable_pde_generator.py, svd_generator.py |
| `EIGENVALUES` | 2 | `EIGENVALUES\|A^T A\|49,4` | low_rank_approx_generator.py, matrix_norm_generator.py, pca_generator.py |
| `EIGENVECTOR` | 2 | `EIGENVECTOR\|A + 1I times v = 0\|[4, 5, 0]` | diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, svd_generator.py |
| `EIGEN_CHECK` | 3 | `EIGEN_CHECK\|sigma_y psi\|-1*psi\|lambda=-1` | spin_half_generator.py |
| `EIGEN_MATRIX` | 2 | `EIGEN_MATRIX\|A + 1I\|[[5, -4, 1], [0, 0, 1], [0, 0, 1]]` | eigenvalue_generator.py |
| `EINSTEIN_SETUP` | 2, 3 | `EINSTEIN_SETUP\|symmetrize\|T_ij=[[-1, 3], [3, 4]]` | einstein_summation_generator.py |
| `ELEC_FORMULA` | 1 | `ELEC_FORMULA\|left charge: E1=q1/r1^2` | electrostatics_generator.py |
| `ELEC_SETUP` | 2, 3 | `ELEC_SETUP\|field_axis\|q1=-7, x1=-3\|q2=-4, x2=3` | electrostatics_generator.py |
| `ELEMENT_ORDER` | 2 | `ELEMENT_ORDER\|8\|9` | cayley_table_generator.py |
| `ELEMENT_SCAN` | 3 | `ELEMENT_SCAN\|30\|A\|found` | set_expression_generator.py, set_membership_subset_generator.py, set_operations_generator.py |
| `ELIMINATE` | 1, 3 | `ELIMINATE\|clue 1\|Dara: book; Iris: spoon; Ravi: stamp; Luca: ticket\|violates clue` | logic_grid_puzzle_generator.py, newtons_laws_generator.py |
| `ELIMINATE_LAMBDA` | 2 | `ELIMINATE_LAMBDA\|f_x = f_y\|y = 2*x` | lagrange_multiplier_generator.py |
| `EL_EQUATION` | 1 | `EL_EQUATION\|mL^2*thetaddot+mgL*sin(theta)=0` | lagrangian_generator.py |
| `EL_SOLVE` | 2 | `EL_SOLVE\|thetaddot\|-(5/3)*sin(theta)` | lagrangian_generator.py |
| `EMBED_SETUP` | 1 | `EMBED_SETUP\|A=(4,3), B=(-5,12), C=(-3,4)` | embedding_similarity_generator.py |
| `ENERGY_FORMULA` | 1 | `ENERGY_FORMULA\|mgh=1/2*m*v^2` | energy_conservation_generator.py |
| `ENERGY_LEVEL` | 2 | `ENERGY_LEVEL\|E_18=hbar*omega*(n+1/2)\|185/2` | ladder_operator_generator.py |
| `ENERGY_SETUP` | 3 | `ENERGY_SETUP\|gravity_drop\|m=10\|h=405, g=10` | energy_conservation_generator.py |
| `ENERGY_TERM` | 1 | `ENERGY_TERM\|T=1/2*m*L^2*thetadot^2` | lagrangian_generator.py |
| `ENGINE_FORMULA` | 1 | `ENGINE_FORMULA\|W=Qh-Qc` | heat_engine_generator.py |
| `ENGINE_SETUP` | 3 | `ENGINE_SETUP\|engine_efficiency\|Qh=290\|Qc=231` | heat_engine_generator.py |
| `ENQUEUE` | 3 | `ENQUEUE\|B\|from D\|B` | graph_traversal_generator.py |
| `ENTER` | 2 | `ENTER\|x\|most negative reduced cost -6` | simplex_generator.py |
| `ENTROPY_FORMULA` | 1 | `ENTROPY_FORMULA\|DeltaS_mix=-sum n_i ln(x_i)` | entropy_change_generator.py |
| `ENTROPY_SETUP` | 2, 3 | `ENTROPY_SETUP\|eigenvalues=[1/8,1/16,1/16,1/128,1/16,1/4,1/128,1/64,1/4,1/32,1/16,1/32,1/64,1/64]\|S=-sum lambda log2(lambda)` | entropy_change_generator.py, entropy_generator.py, huffman_coding_generator.py, information_gain_generator.py, mutual_information_generator.py, von_neumann_entropy_generator.py |
| `ENTROPY_SKIP` | 2 | `ENTROPY_SKIP\|H(X,Y)\|p=0` | mutual_information_generator.py |
| `ENTROPY_TERM` | 4 | `ENTROPY_TERM\|row 0\|p=3/4\|I=0.415\|249/800` | entropy_rate_markov_generator.py |
| `ENTROPY_VALUE` | 2 | `ENTROPY_VALUE\|parent\|0.81125` | information_gain_generator.py |
| `ENTROPY_ZERO` | 2 | `ENTROPY_ZERO\|texture_right\|count=0` | information_gain_generator.py |
| `EPSILON_VALUE` | 2 | `EPSILON_VALUE\|eps_123\|1` | index_gymnastics_generator.py |
| `EPS_CLOSURE` | 2 | `EPS_CLOSURE\|{p1}\|{p1}` | nfa_simulation_generator.py |
| `EQUATE_EXP` | 1 | `EQUATE_EXP\|2x + 2 = 4` | exponential_equation_generator.py |
| `EQUILIBRIA` | 2 | `EQUILIBRIA\|f(y) = 0\|y=-11, y=0` | stability_generator.py |
| `EQ_2PT_SETUP` | 2 | `EQ_2PT_SETUP\|(-8, 9)\|(-9, 9)` | equation_from_two_points_generator.py |
| `EQ_OP_BOTH` | 3, 4 | `EQ_OP_BOTH\|multiply\|6\|x\|42` | absolute_value_equation_generator.py, area_between_curves_generator.py, completing_square_generator.py, curve_analysis_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, implicit_diff_generator.py, inverse_function_generator.py, linear_fractional_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, mean_value_theorem_generator.py, one_step_equation_generator.py, optimization_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, separable_ode_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_OP_NOTE` | 3 | `EQ_OP_NOTE\|subtract\|r\|from both sides` | equation_from_two_points_generator.py, literal_equation_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `EQ_RESULT` | 2 | `EQ_RESULT\|x\|42` | completing_square_generator.py, error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, linear_simple_generator.py, one_step_equation_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, special_solution_equation_generator.py, two_step_equation_generator.py |
| `EQ_SETUP` | 1, 2 | `EQ_SETUP\|x = 6/2` | area_between_curves_generator.py, completing_square_generator.py, complex_quadratic_generator.py, cramers_rule_generator.py, discriminant_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_equation_generator.py, one_step_equation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, remainder_factor_theorem_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_SIMPLIFY` | 1 | `EQ_SIMPLIFY\|x/3 = 1` | error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, two_step_equation_generator.py |
| `ESCAPE_CHECK` | 3 | `ESCAPE_CHECK\|n=1\|norm2=305/16\|escaped` | fractal_iteration_generator.py |
| `ESTIMATE` | 2 | `ESTIMATE\|68780 × 53343 ≈ 70000 × 50000\|3500000000` | long_division_generator.py, multi_digit_multiplication_generator.py |
| `ESTIMATE_CHECK` | 3 | `ESTIMATE_CHECK\|7.2 × 10^4\|72000\|rounded estimate` | fermi_estimation_generator.py, long_division_generator.py, multi_digit_multiplication_generator.py |
| `EUCLID_DIV` | 4 | `EUCLID_DIV\|48\|35\|1\|13` | continued_fraction_generator.py, extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `EULER_BACKTRACK` | 3 | `EULER_BACKTRACK\|E\|route suffix E\|stack C-B-A-E-C-D` | euler_circuit_generator.py |
| `EULER_CRITERION` | 2 | `EULER_CRITERION\|3^20 mod 41\|40` | quadratic_residue_generator.py |
| `EULER_FORMULA` | 1 | `EULER_FORMULA\|χ = V - E + F` | euler_characteristic_generator.py, euler_formula_generator.py |
| `EULER_NOTE` | 2 | `EULER_NOTE\|2\|sphere-family polyhedron: χ is always 2` | euler_characteristic_generator.py |
| `EULER_ROUTE` | 2 | `EULER_ROUTE\|C-B-A-E-C-D-E\|uses 6 edges` | euler_circuit_generator.py |
| `EULER_SETUP` | 2, 3 | `EULER_SETUP\|square pyramid: V = 5, E = 8, F = 5\|V - E + F` | euler_characteristic_generator.py, euler_formula_generator.py |
| `EULER_STACK` | 2 | `EULER_STACK\|initial\|C` | euler_circuit_generator.py |
| `EULER_START` | 2 | `EULER_START\|C\|alphabetically first odd vertex` | euler_circuit_generator.py |
| `EULER_TRAVERSE` | 3 | `EULER_TRAVERSE\|C->B\|BC\|stack C-B` | euler_circuit_generator.py |
| `EVAL` | 1, 2, 3 | `EVAL\|g(-6)\|-36` | arc_length_generator.py, area_between_curves_generator.py, circle_equation_generator.py, complex_division_generator.py, composite_arithmetic_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dot_product_generator.py, ellipse_features_generator.py, euler_method_generator.py, exact_ode_generator.py, five_number_summary_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, improper_integral_generator.py, lagrange_multiplier_generator.py, legendre_construction_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_properties_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, ode_substitution_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, power_series_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, row_reduction_generator.py, runge_kutta_generator.py, solid_revolution_generator.py, standard_deviation_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py |
| `EVAL_AT_ZERO` | 2 | `EVAL_AT_ZERO\|e^0=1\|e^(2*0)=1` | mgf_generator.py |
| `EVAL_PARTIAL` | 3 | `EVAL_PARTIAL\|f_x\|10*2 - 2*4 + 2\|14` | gradient_generator.py, multivar_chain_rule_generator.py |
| `EVAL_SUB` | 3 | `EVAL_SUB\|p=T, q=T\|formula: ¬q\|F` | set_identity_membership_table_generator.py, truth_table_generator.py |
| `EVENT` | 2, 3 | `EVENT\|A\|first 11 tickets\|11` | complement_probability_generator.py, fundamental_counting_principle_generator.py, probability_axioms_finite_generator.py, sample_space_list_generator.py, simple_probability_generator.py |
| `EV_FORMULA` | 1 | `EV_FORMULA\|E[X] = Σ x·P(x)` | expected_value_generator.py |
| `EV_SETUP` | 2 | `EV_SETUP\|P(X=0) = 3/10; P(X=2) = 1/10; P(X=1) = 3/5\|Var(X)` | expected_value_generator.py |
| `EXACT_MATCH` | 2 | `EXACT_MATCH\|F_y = N\|-4*x + g'(y) = -4*x + 10*y - 4` | exact_ode_generator.py |
| `EXPAND` | 1, 2 | `EXPAND\|h = pt\|h = (ex)t` | complex_locus_generator.py, direct_proof_algebra_generator.py, mobius_transform_generator.py, zf_axiom_identify_generator.py |
| `EXPECTATION` | 3 | `EXPECTATION\|E[X]=31/36\|E[Y]=31/36\|E[XY]=1519/1944` | joint_distribution_generator.py |
| `EXPECTED_PAYOFF` | 1 | `EXPECTED_PAYOFF\|row1 against q` | game_theory_generator.py |
| `EXP_APPLY` | 2 | `EXP_APPLY\|x(t) = e^(At)x(0)\|x(0) = [-3, 5]` | matrix_exponential_generator.py |
| `EXP_CELL` | 2 | `EXP_CELL\|(80·30)/100\|24` | chi_square_generator.py |
| `EXP_DIAG` | 2 | `EXP_DIAG\|e^(Dt)\|[[e^(3t), 0], [0, e^(6t)]]` | matrix_exponential_generator.py |
| `EXP_ENTRY` | 3 | `EXP_ENTRY\|(1,1)\|-4*e^(3t) + 5*e^(6t)\|-4*e^(3t) + 5*e^(6t)` | matrix_exponential_generator.py |
| `EXP_EXPAND` | 1 | `EXP_EXPAND\|5 × 5 × 5 × 5` | exponent_generator.py |
| `EXP_FORM` | 1 | `EXP_FORM\|e^(At) = P*e^(Dt)*P^-1` | euler_formula_generator.py, matrix_exponential_generator.py |
| `EXP_PARTIAL` | 3 | `EXP_PARTIAL\|5\|5\|25` | exponent_generator.py |
| `EXP_RULE_APPLY` | 3, 4 | `EXP_RULE_APPLY\|multiply\|5\|11\|55` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_RULE_IDENTIFY` | 2 | `EXP_RULE_IDENTIFY\|power_rule\|(x^a)^b = x^(ab)` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SETUP` | 1 | `EXP_RULE_SETUP\|(y^5)^11` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SIMPLIFY` | 1 | `EXP_RULE_SIMPLIFY\|y^55` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_SETUP` | 2 | `EXP_SETUP\|5\|4` | exponent_generator.py |
| `EXP_SUB` | 3 | `EXP_SUB\|t/tau\|1\|e^-1` | transient_circuit_generator.py |
| `EXP_VALUE` | 2 | `EXP_VALUE\|exp(-z)\|1` | activation_generator.py |
| `EXT_GCD_SETUP` | 2 | `EXT_GCD_SETUP\|48\|35` | extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `F` | 2, 3 | `F\|4/6\|2/3` | complement_probability_generator.py, composite_arithmetic_generator.py, counting_to_probability_generator.py, derangement_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, fundamental_counting_principle_generator.py, likelihood_language_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, order_of_operations_generator.py, quaternion_generator.py, radical_rationalize_generator.py, random_digit_simulation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, repeating_decimal_generator.py, sample_space_list_generator.py, simple_probability_generator.py, slope_two_points_generator.py, two_way_table_probability_generator.py, venn_probability_generator.py |
| `FACT` | 2 | `FACT\|7\|5040` | counting_to_probability_generator.py, derangement_generator.py, named_distribution_generator.py, order_statistics_generator.py, young_tableaux_generator.py |
| `FACTOR` | 1, 2 | `FACTOR\|h = e(xt)` | direct_proof_algebra_generator.py, polynomial_inequality_generator.py, second_order_ode_generator.py, transfer_function_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `FACTOR_FORM` | 2 | `FACTOR_FORM\|29\|29` | totient_generator.py |
| `FACTOR_FOUND` | 2 | `FACTOR_FOUND\|29\|1` | totient_generator.py |
| `FACTOR_GROUP` | 3 | `FACTOR_GROUP\|6y^2 + 4y\|2y\|(3y + 2)` | conic_standard_form_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, factor_grouping_generator.py, factor_trinomial_generator.py |
| `FACTOR_PAIR_GOAL` | 2 | `FACTOR_PAIR_GOAL\|m·n = 32\|m + n = 12` | factor_trinomial_generator.py |
| `FACTOR_SETUP` | 1 | `FACTOR_SETUP\|29` | totient_generator.py |
| `FACT_CHECK` | 3 | `FACT_CHECK\|375\|1\|0` | factors_generator.py |
| `FACT_FORMULA` | 1 | `FACT_FORMULA\|7! = 1·2·3·4·5·6·7` | derangement_generator.py, permutation_combination_generator.py |
| `FACT_PAIR` | 2 | `FACT_PAIR\|1\|375` | factors_generator.py |
| `FACT_SETUP` | 2 | `FACT_SETUP\|7!\|expand the factorial` | permutation_combination_generator.py |
| `FACT_VALUE` | 2 | `FACT_VALUE\|8!\|40320` | stars_and_bars_generator.py |
| `FCP` | 3 | `FCP\|fruits\|11\|11` | counting_to_probability_generator.py, fundamental_counting_principle_generator.py |
| `FEATURE_MAP_SETUP` | 3 | `FEATURE_MAP_SETUP\|K(x,z)=(xz+2)^2\|phi(t)=(t^2,2t,2)\|x=16,z=-17` | feature_map_generator.py |
| `FEATURE_VECTOR` | 2 | `FEATURE_VECTOR\|phi(x)\|(256,32,2)` | feature_map_generator.py |
| `FEEDBACK` | 1 | `FEEDBACK\|T=G/(1+G)` | transfer_function_generator.py |
| `FERMAT_SETUP` | 3 | `FERMAT_SETUP\|prime 13\|base 43\|exponent 165` | totient_generator.py |
| `FERMI_FACTOR` | 2 | `FERMI_FACTOR\|students\|1200` | fermi_estimation_generator.py |
| `FERMI_SETUP` | 2 | `FERMI_SETUP\|school pizza slices\|slices/year` | fermi_estimation_generator.py |
| `FIELD_SETUP` | 2 | `FIELD_SETUP\|GF(2)[x]\|addition is XOR` | finite_field_generator.py |
| `FIND_SLOPE` | 2 | `FIND_SLOPE\|Given slope (m1)\|-2/3` | parallel_perpendicular_line_generator.py |
| `FINITE_DIFF_SETUP` | 3 | `FINITE_DIFF_SETUP\|central_derivative\|x0=4,h=2\|f-=17,f+=125` | finite_difference_generator.py |
| `FIN_FORMULA` | 1 | `FIN_FORMULA\|I = P*r*t; A = P + I` | finance_generator.py |
| `FIN_SETUP` | 3 | `FIN_SETUP\|simple interest P = 200\|r = 6%, t = 4\|interest and balance` | finance_generator.py |
| `FIRSTLAW_FORMULA` | 1 | `FIRSTLAW_FORMULA\|W=P*(V2-V1)` | first_law_generator.py |
| `FIRSTLAW_SETUP` | 3 | `FIRSTLAW_SETUP\|isobaric\|P=3, V1=3, V2=2\|Q=49` | first_law_generator.py |
| `FIXED_CHECK` | 3 | `FIXED_CHECK\|b\|f(b) = r\|not fixed` | function_properties_generator.py |
| `FIXED_EQ` | 1 | `FIXED_EQ\|z=(az+b)/(cz+d)` | mobius_transform_generator.py |
| `FIXED_POINT` | 1 | `FIXED_POINT\|1` | mobius_transform_generator.py |
| `FIXED_POINT_SETUP` | 3 | `FIXED_POINT_SETUP\|g(x)=1/9*x-2\|x0=1\|iterations=3` | fixed_point_generator.py |
| `FIXED_POINT_UPDATE` | 3 | `FIXED_POINT_UPDATE\|1\|x_0=1\|x_1=-17/9` | fixed_point_generator.py |
| `FLAG` | 2 | `FLAG\|8\|right F` | error_spotting_generator.py, foundations_critic_generator.py |
| `FLIP` | 2 | `FLIP\|1\|1 → 0` | cantor_diagonal_generator.py |
| `FLOOR_DIV` | 3 | `FLOOR_DIV\|5\|2\|2` | algorithm_trace_generator.py |
| `FLOPS_SETUP` | 2 | `FLOPS_SETUP\|rule=2mnk\|m=16,d=128,h=256,o=512` | flops_memory_generator.py |
| `FLUX_SUM` | 2 | `FLUX_SUM\|(-5 - 4 + 2)*216\|-1512` | vector_theorem_generator.py |
| `FOCUS` | 1 | `FOCUS\|(2, -6)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `FOIL_F` | 2 | `FOIL_F\|First: (-9) * 3\|-27` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_I` | 2 | `FOIL_I\|Inner: (-6i) * 3\|-18i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_L` | 2 | `FOIL_L\|Last: (-6i) * 8i\|-48i^2` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_O` | 2 | `FOIL_O\|Outer: (-9) * 8i\|-72i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_SETUP` | 1 | `FOIL_SETUP\|(6 + √6)(4 + √6)` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py, radical_multiply_generator.py, trig_identity_verify_generator.py |
| `FOLD` | 2 | `FOLD\|gcd(3, 1)\|1` | peano_arithmetic_generator.py, recursive_definition_unfold_generator.py |
| `FORCE_COMPONENT` | 1 | `FORCE_COMPONENT\|parallel=m*g*sin` | newtons_laws_generator.py |
| `FORCE_EQ` | 1 | `FORCE_EQ\|m*a=parallel-friction` | newtons_laws_generator.py |
| `FORM` | 2 | `FORM\|inverse\|If n ≤ 133, then n ≤ 87.` | conditional_forms_generator.py, zf_axiom_identify_generator.py |
| `FORMULA` | 1, 2 | `FORMULA\|sinh x = (e^x - e^(-x))/2` | collision_generator.py, gaussian_curvature_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, or_formula_generator.py, projectile_motion_generator.py, stereographic_generator.py, uncertainty_generator.py |
| `FORM_IDENTIFY` | 2 | `FORM_IDENTIFY\|perfect_square_trinomial\|a^2 + 2ab + b^2 = (a + b)^2` | completing_square_generator.py, conic_standard_form_generator.py, ellipse_features_generator.py, factor_special_forms_generator.py, hyperbola_features_generator.py, parabola_features_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py |
| `FOURIER_COEF` | 1 | `FOURIER_COEF\|b_3=8/pi` | fourier_series_generator.py |
| `FOURIER_SETUP` | 3 | `FOURIER_SETUP\|square\|A=6\|n=3` | fourier_series_generator.py |
| `FOUR_VECTOR_SETUP` | 3 | `FOUR_VECTOR_SETUP\|mass_shell\|c=1\|p=15, m=8` | four_vector_generator.py |
| `FRACTAL_SETUP` | 4 | `FRACTAL_SETUP\|julia\|z0=(-3/2,-1)\|c=(1/2,1)\|N=6` | fractal_iteration_generator.py |
| `FRAC_BUILD` | 2 | `FRAC_BUILD\|50/110\|5/11` | conditional_probability_generator.py, geometric_probability_generator.py, two_way_table_probability_generator.py |
| `FRAC_REDUCE` | 2 | `FRAC_REDUCE\|14/12\|7/6` | angle_measure_generator.py, arc_length_generator.py, arc_sector_generator.py, complex_division_generator.py, frequency_table_generator.py, function_operations_generator.py, hyperbola_features_generator.py, implicit_diff_generator.py, improper_integral_generator.py, probability_addition_rule_generator.py, related_rates_generator.py, right_triangle_trig_generator.py |
| `FRAC_TO_DEC` | 2 | `FRAC_TO_DEC\|43/40\|1.075` | fraction_decimal_percent_converter.py, simple_probability_generator.py |
| `FREQ_SETUP` | 2 | `FREQ_SETUP\|histogram — 60-69: 13, 70-79: 7, 80-89: 14, 90-99: 12\|cumulative count up to 90-99` | frequency_table_generator.py |
| `FUNC_OP` | 2 | `FUNC_OP\|(g · h)(-6)\|g(-6) · h(-6)` | function_composition_generator.py, function_operations_generator.py |
| `FUNC_SETUP` | 2 | `FUNC_SETUP\|x: -4, -3, -2, 5, 6; g(x): -1, 17, 16, -2, 20\|g(5)` | domain_range_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, inverse_function_generator.py, piecewise_evaluation_generator.py, rational_function_features_generator.py |
| `FUNDAMENTAL_FORM_SETUP` | 3 | `FUNDAMENTAL_FORM_SETUP\|cylinder\|R=2\|u in [0,2pi/3], v in [0,3]` | fundamental_form_generator.py |
| `GAME_SETUP` | 2 | `GAME_SETUP\|payoffs=(1,15;15,7)\|row player maximizes, column player minimizes` | game_theory_generator.py |
| `GAMMA_SETUP` | 3 | `GAMMA_SETUP\|trace\|gamma0,gamma0\|Tr(product)` | gamma_matrix_generator.py |
| `GAS_FORMULA` | 1 | `GAS_FORMULA\|P1*V1/T1=P2*V2/T2` | gas_law_generator.py, gas_stoichiometry_generator.py |
| `GAS_SETUP` | 3 | `GAS_SETUP\|combined_pressure\|P1=19, V1=13, T1=21\|V2=12, T2=21` | gas_law_generator.py |
| `GAS_STOICH_SETUP` | 3 | `GAS_STOICH_SETUP\|mass_to_gas_volume\|2 H2O2 -> 2 H2O + O2\|given=68 g H2O2, gas=O2` | gas_stoichiometry_generator.py |
| `GATE_MATRIX` | 2 | `GATE_MATRIX\|H\|(1/sqrt(2))*[[1,1],[1,-1]]` | quantum_gate_generator.py |
| `GAUSSIAN_CURVATURE_SETUP` | 2, 3 | `GAUSSIAN_CURVATURE_SETUP\|sphere\|R=118` | gaussian_curvature_generator.py |
| `GAUSS_BONNET_SETUP` | 3 | `GAUSS_BONNET_SETUP\|flat_torus\|width=9, height=4\|chi=0` | gauss_bonnet_generator.py |
| `GAUSS_FORMULA` | 1 | `GAUSS_FORMULA\|2*E*A=sigma*A` | gauss_law_generator.py |
| `GAUSS_SETUP` | 3 | `GAUSS_SETUP\|sheet_charge\|sigma=53\|A=24` | gauss_law_generator.py |
| `GCD` | 2 | `GCD\|gcd(265,720)\|5` | derangement_generator.py, pollard_factorization_generator.py |
| `GCD_DIV` | 4 | `GCD_DIV\|127\|55\|2\|17` | rationals_as_pairs_generator.py |
| `GCD_DONE` | 1 | `GCD_DONE\|1` | rationals_as_pairs_generator.py |
| `GCD_RESULT` | 1, 2 | `GCD_RESULT\|1` | lcm_generator.py, modular_inverse_generator.py, permutation_group_generator.py, rsa_generator.py, totient_generator.py |
| `GCD_START` | 2 | `GCD_START\|45\|118` | gcf_generator.py, lcm_generator.py, rationals_as_pairs_generator.py |
| `GCD_STEP` | 3 | `GCD_STEP\|45\|118\|45` | gcf_generator.py, lcm_generator.py |
| `GCF_COEFF` | 2 | `GCF_COEFF\|12, 54\|6` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_RESULT` | 1 | `GCF_RESULT\|6` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_VAR` | 2 | `GCF_VAR\|y^5, y^3, y^2\|y^2` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GD_SETUP` | 3 | `GD_SETUP\|f(x,y)=1/2*(4x^2+5y^2)\|start=(-6,-1)\|eta=1/11` | gradient_descent_generator.py |
| `GD_UPDATE` | 3 | `GD_UPDATE\|w_old=(-3,3)\|eta=1/8\|w_new=(-15/4,-5/3)` | gradient_step_generator.py |
| `GELLMANN_IDENTITY` | 3 | `GELLMANN_IDENTITY\|Tr(lambda_7 lambda_2)\|2 delta_ab\|0` | pauli_algebra_generator.py |
| `GELLMANN_SETUP` | 3 | `GELLMANN_SETUP\|trace\|A=-lambda_7\|B=4lambda_2` | pauli_algebra_generator.py |
| `GENERAL` | 2 | `GENERAL\|a_n\|C1(-2)^n + C2(-3)^n - 1` | recurrence_generator.py |
| `GEOMETRIC_FORMULA` | 2 | `GEOMETRIC_FORMULA\|c_n = A*(-1)^n/d^(n+1)\|A=1, d=2` | laurent_series_generator.py |
| `GEOM_FORMULA` | 1 | `GEOM_FORMULA\|E[X] = 1/p` | geometric_distribution_generator.py |
| `GEOM_SETUP` | 2 | `GEOM_SETUP\|p = 1/6\|E[X]` | geometric_distribution_generator.py |
| `GEO_PROB_FORMULA` | 1 | `GEO_PROB_FORMULA\|probability = sector angle / 360` | geometric_probability_generator.py |
| `GEO_PROB_SETUP` | 2 | `GEO_PROB_SETUP\|full circle\|sector angle 144°` | geometric_probability_generator.py |
| `GEO_SETUP` | 2 | `GEO_SETUP\|right triangle, altitude h = 59 to the hypotenuse; one segment p = 59\|the other segment q` | geometric_mean_generator.py |
| `GF2_XOR` | 3 | `GF2_XOR\|quotient x^3\|0 xor 1\|1` | finite_field_generator.py |
| `GF_DIV_CHECK` | 3 | `GF_DIV_CHECK\|18 / 4\|not integer\|reject` | generating_function_generator.py |
| `GF_EXPAND` | 2 | `GF_EXPAND\|(1 + x)^3\|sum C(a,i)x^i` | generating_function_generator.py |
| `GF_SETUP` | 2 | `GF_SETUP\|[x^2]\|(1 + x)^3(1 + x)^5` | generating_function_generator.py |
| `GIANT_FACTOR` | 2 | `GIANT_FACTOR\|g^-m mod p\|2` | baby_step_giant_step_generator.py |
| `GIANT_STEP` | 2 | `GIANT_STEP\|i=0\|7` | baby_step_giant_step_generator.py |
| `GLB` | 1 | `GLB\|{a}` | partial_order_generator.py |
| `GOAL` | 1 | `GOAL\|show n + 1 is even` | direct_proof_algebra_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `GODEL_DECODE` | 2 | `GODEL_DECODE\|5, 5, 4\|) ) (` | godel_numbering_generator.py |
| `GODEL_TERM` | 2 | `GODEL_TERM\|2^4\|16` | godel_numbering_generator.py |
| `GRAD` | 2 | `GRAD\|1\|1/6` | softmax_gradient_generator.py |
| `GRADIENT_FORMULA` | 1 | `GRADIENT_FORMULA\|grad=(4x,5y)` | gradient_descent_generator.py, matrix_calculus_generator.py |
| `GRAD_ENTRY` | 2 | `GRAD_ENTRY\|g1\|56` | matrix_calculus_generator.py |
| `GRAD_RESULT` | 2 | `GRAD_RESULT\|grad g\|(2, 5)` | lagrange_multiplier_generator.py |
| `GRAD_SETUP` | 3 | `GRAD_SETUP\|f(x,y) = 5*x^2 + 5*y^2 - 2*x*y + 2*x - 4*y\|point (2, 4)\|gradient` | gradient_generator.py |
| `GRAPH_CHANGE` | 3 | `GRAPH_CHANGE\|2018\|2019\|8` | graph_interpret_generator.py |
| `GRAPH_DATA` | 2 | `GRAPH_DATA\|bar_chart\|History:16,Math:12,Music:26,English:47` | graph_interpret_generator.py |
| `GRAPH_MAX` | 2 | `GRAPH_MAX\|Buses\|80` | graph_interpret_generator.py |
| `GRAPH_MAX_CHANGE` | 3 | `GRAPH_MAX_CHANGE\|2021\|2022\|-5` | graph_interpret_generator.py |
| `GRAPH_MIN` | 2 | `GRAPH_MIN\|Mon\|21` | graph_interpret_generator.py |
| `GRAPH_READ` | 2 | `GRAPH_READ\|History\|16` | graph_interpret_generator.py |
| `GRAPH_SETUP` | 2 | `GRAPH_SETUP\|vertices A, B, C, D, E\|edges AC, AE, BE, CD, CE, DE` | dijkstra_generator.py, euler_circuit_generator.py, graph_counting_generator.py, graph_traversal_generator.py |
| `GRASSMANN_RESULT` | 3 | `GRASSMANN_RESULT\|constant=-32\|theta=80\|-32 + 80theta` | grassmann_generator.py |
| `GRASSMANN_SETUP` | 3 | `GRASSMANN_SETUP\|multiply\|x=4 - 6theta\|y=-8 + 8theta` | grassmann_generator.py |
| `GREATEST` | 1 | `GREATEST\|none` | partial_order_generator.py |
| `GREAT_CIRCLE_SETUP` | 3 | `GREAT_CIRCLE_SETUP\|R=6\|A=(0,-60)\|B=(0,120)` | great_circle_generator.py |
| `GROUP` | 2 | `GROUP\|(6y^2 + 4y)\|(15y + 10)` | factor_grouping_generator.py, factor_trinomial_generator.py |
| `GROUP_MULT` | 3 | `GROUP_MULT\|e\|e\|e` | coset_generator.py |
| `GROUP_SETUP` | 2, 3 | `GROUP_SETUP\|Z_9\|addition mod n` | cayley_table_generator.py, coset_generator.py, cyclic_group_generator.py |
| `GS_SETUP` | 2 | `GS_SETUP\|vectors [[-2, -1], [7, 1]]\|orthogonal basis, not normalized` | gram_schmidt_generator.py |
| `GS_SUBTRACT` | 2 | `GS_SUBTRACT\|remove projection on u1\|[1, -2]` | gram_schmidt_generator.py, qr_decomposition_generator.py |
| `GS_VECTOR` | 2 | `GS_VECTOR\|u1 = v1\|[-2, -1]` | gram_schmidt_generator.py |
| `HA` | 1 | `HA\|y = 5/2` | rational_function_features_generator.py |
| `HAMILTON` | 2 | `HAMILTON\|i*i\|-1` | quaternion_generator.py |
| `HAMILTONIAN` | 1 | `HAMILTONIAN\|H=p_x^2/(2m)+1/2*k*x^2` | hamiltonian_generator.py |
| `HAMMING_PLACE` | 2 | `HAMMING_PLACE\|positions 1,2,3,4,5,6,7\|p1,p2,d1,p4,d2,d3,d4` | hamming_code_generator.py |
| `HAMMING_RECEIVED` | 1 | `HAMMING_RECEIVED\|r=1000000` | hamming_code_generator.py |
| `HAMMING_SETUP` | 2 | `HAMMING_SETUP\|data=1000\|even parity` | hamming_code_generator.py |
| `HAM_EQ` | 2 | `HAM_EQ\|xdot=dH/dp_x\|xdot=p_x/4` | hamiltonian_generator.py |
| `HAM_SETUP` | 3 | `HAM_SETUP\|mass_spring\|m=4, k=23\|q=x, p=p_x` | hamiltonian_generator.py |
| `HARMONIC_SETUP` | 1 | `HARMONIC_SETUP\|u=-3x^2 + 3y^2 + x + 3y` | cauchy_riemann_generator.py |
| `HAWKING_SETUP` | 3 | `HAWKING_SETUP\|entropy\|S_BH=k_B*c^3*A/(4*hbar*G)\|k_B=5,c=5,A=69,hbar=11,G=12` | hawking_generator.py |
| `HESSIAN_DET` | 3 | `HESSIAN_DET\|D = f_xx*f_yy - f_xy^2\|(-4)*(-8) - (-3)^2\|23` | hessian_classify_generator.py |
| `HESSIAN_SETUP` | 2 | `HESSIAN_SETUP\|f(x,y) = -2*x^2 - 4*y^2 - 3*x*y\|find and classify the critical point` | hessian_classify_generator.py |
| `HESSIAN_TEST` | 3 | `HESSIAN_TEST\|D = 23\|f_xx = -4\|local maximum` | hessian_classify_generator.py |
| `HIDDEN_PRE` | 2 | `HIDDEN_PRE\|h1\|z=-3` | backprop_generator.py |
| `HIT_EQ` | 2 | `HIT_EQ\|t0=1+p00*t0+p01*t1\|t1=1+p10*t0+p11*t1` | markov_chain_generator.py |
| `HMM_SETUP` | 2 | `HMM_SETUP\|states H,L\|observations BAA` | viterbi_generator.py |
| `HMM_START` | 1 | `HMM_START\|H=1/2, L=1/2` | viterbi_generator.py |
| `HOLE` | 1 | `HOLE\|x = -3` | rational_function_features_generator.py |
| `HOM_SOL` | 2 | `HOM_SOL\|y_h\|y_h = C1e^(-3x) + C2e^(-x)` | undetermined_coeff_generator.py, variation_parameters_generator.py |
| `HOOK` | 4 | `HOOK\|(1,1)\|right=2\|below=4\|hook=7` | young_tableaux_generator.py |
| `HORNER_SETUP` | 2 | `HORNER_SETUP\|x^3 - 2x^2 - 3x + 2\|x = 3` | horner_evaluation_generator.py |
| `HT_SETUP` | 2 | `HT_SETUP\|H0: p = 0.5; Ha: p ≠ 0.5\|n = 100, 57 successes, critical value = 1.96` | hypothesis_test_generator.py, two_sample_test_generator.py |
| `HUFFMAN_FORMULA` | 1 | `HUFFMAN_FORMULA\|L=sum p_i*l_i` | huffman_coding_generator.py |
| `HUFFMAN_MERGE` | 2 | `HUFFMAN_MERGE\|B:1/8 + C:1/8\|BC:1/4` | huffman_coding_generator.py |
| `HUFFMAN_SETUP` | 1 | `HUFFMAN_SETUP\|A=1/4, B=1/8, C=1/8, D=1/2` | huffman_coding_generator.py |
| `HYDROGEN_FORMULA` | 1 | `HYDROGEN_FORMULA\|E_ion=R_E/n^2` | hydrogen_atom_generator.py |
| `HYDROGEN_SETUP` | 3 | `HYDROGEN_SETUP\|ionization_energy\|n=10\|R_E=21 eV` | hydrogen_atom_generator.py |
| `HYPERBOLIC_DISTANCE_SETUP` | 3 | `HYPERBOLIC_DISTANCE_SETUP\|disk\|P=(0,0)\|Q=(7/33,0)` | hyperbolic_distance_generator.py |
| `HYPERBOLIC_SETUP` | 2 | `HYPERBOLIC_SETUP\|e^x=17/3\|e^(-x)=3/17` | hyperbolic_function_generator.py |
| `HYPERCUBE_FORMULA` | 1 | `HYPERCUBE_FORMULA\|k-faces of the n-cube: C(n,k) · 2^(n-k)` | hypercube_counting_generator.py |
| `HYPERCUBE_SETUP` | 2 | `HYPERCUBE_SETUP\|3-cube\|number of square faces (k = 2)` | hypercube_counting_generator.py |
| `I` | 2 | `I\|7/2\|2/7` | fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_mult_div_generator.py |
| `ICE_ROW` | 2 | `ICE_ROW\|initial\|[A]=4, [B]=0` | equilibrium_ice_generator.py |
| `IDENTIFY` | 2 | `IDENTIFY\|order does not matter\|use C(n, r)` | permutation_combination_generator.py |
| `IDENTITY` | 2 | `IDENTITY\|Vandermonde\|Σ C(16,i)C(8,11-i) = C(24,11)` | counting_classics_generator.py, function_inner_product_generator.py, index_gymnastics_generator.py |
| `IDENTITY_SETUP` | 2 | `IDENTITY_SETUP\|verify: (1 + tan^2 x) · cos^2 x = 1\|transform the left side` | trig_identity_verify_generator.py |
| `IDENT_MATCH` | 1 | `IDENT_MATCH\|1 = 1` | trig_identity_verify_generator.py |
| `IDENT_SUB` | 1, 2 | `IDENT_SUB\|1 + tan^2 x = sec^2 x` | parametric_calculus_generator.py, trig_identity_verify_generator.py |
| `IE_FORMULA` | 1, 2 | `IE_FORMULA\|count(R or C) = count(R) + count(C) − count(R and C)` | inclusion_exclusion_generator.py, probability_measure_generator.py, two_way_table_probability_generator.py, venn_probability_generator.py |
| `IE_SETUP` | 2 | `IE_SETUP\|n(A)=39, n(B)=28\|n(A intersect B)=18` | inclusion_exclusion_generator.py |
| `IFACTOR` | 2 | `IFACTOR\|mu = e^(∫ 5 dx)\|e^(5x)` | integrating_factor_generator.py, ode_substitution_generator.py |
| `IG_SETUP` | 3 | `IG_SETUP\|parent pos=4, neg=12\|total=16\|splits=source,texture` | information_gain_generator.py |
| `IMAGE` | 2 | `IMAGE\|e\|14` | function_properties_generator.py, mobius_transform_generator.py |
| `IMPLICIT_DIFF` | 2 | `IMPLICIT_DIFF\|d/dx of x^2\|2x` | implicit_diff_generator.py, log_diff_higher_order_generator.py, related_rates_generator.py |
| `IMPLICIT_SETUP` | 2 | `IMPLICIT_SETUP\|x^2 + xy + y^2 = 27\|dy/dx` | implicit_diff_generator.py |
| `IMPROPER_TO_MIX` | 2 | `IMPROPER_TO_MIX\|477/55\|8 37/55` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `INDEGREE` | 2 | `INDEGREE\|A\|0` | graph_traversal_generator.py |
| `INDEGREE_UPDATE` | 2 | `INDEGREE_UPDATE\|B\|0` | graph_traversal_generator.py |
| `INDEP_CHECK` | 3 | `INDEP_CHECK\|P11=1519/1944\|product=961/1296\|no` | joint_distribution_generator.py |
| `INDEP_FORMULA` | 1 | `INDEP_FORMULA\|independent iff P11=P(X=1)P(Y=1)` | joint_distribution_generator.py |
| `INDEX` | 3 | `INDEX\|G size 20\|H size 10\|2` | coset_generator.py |
| `INDEX_METRIC` | 3 | `INDEX_METRIC\|raise\|Minkowski\|g^ii=[-1,1,1,1]` | index_raising_generator.py |
| `INDEX_SETUP` | 3 | `INDEX_SETUP\|c=-5\|j=2, k=3\|l=2, m=2` | index_gymnastics_generator.py |
| `INDUCT_ASSUME` | 1, 2 | `INDUCT_ASSUME\|n = 4a + 5b\|a,b nonnegative` | induction_verify_generator.py |
| `INDUCT_BASE` | 2 | `INDUCT_BASE\|n=12\|12 = 4·3 + 5·0` | induction_verify_generator.py |
| `INDUCT_STEP` | 1, 2 | `INDUCT_STEP\|n → n+4\|n+4 = 4(a+1) + 5b` | induction_verify_generator.py |
| `INEQ_FLIP` | 1 | `INEQ_FLIP\|Dividing by negative number reverses inequality` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_OP_ALL` | 3 | `INEQ_OP_ALL\|subtract\|6\|-14 ≤ 1x ≤ 2` | absolute_value_inequality_generator.py, compound_inequality_generator.py |
| `INEQ_OP_BOTH` | 4 | `INEQ_OP_BOTH\|subtract\|8\|x\|3` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_RESULT` | 3 | `INEQ_RESULT\|x\|>\|3` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SETUP` | 1 | `INEQ_SETUP\|x + 8 > 11` | linear_fractional_generator.py, one_step_inequality_generator.py, polynomial_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SIMPLIFY` | 1 | `INEQ_SIMPLIFY\|6x > 12` | domain_range_generator.py, linear_fractional_generator.py, two_step_inequality_generator.py |
| `INEX_TERM` | 3 | `INEX_TERM\|0\|1×4^6\|4096` | function_properties_generator.py |
| `INFO_GAIN` | 2 | `INFO_GAIN\|source\|0` | information_gain_generator.py |
| `INFO_SETUP` | 2 | `INFO_SETUP\|p=1/32768\|I=-log2(p)` | entropy_generator.py |
| `INFO_TABLE` | 1 | `INFO_TABLE\|1/4=2, 1/2=1, 3/4=0.415, 1=0` | information_gain_generator.py |
| `INFO_VALUE` | 2 | `INFO_VALUE\|p=1/4\|I=2` | information_gain_generator.py |
| `INITIAL` | 2 | `INITIAL\|D_0 = 1\|D_1 = 0` | derangement_generator.py |
| `INITIAL_COEFF` | 2 | `INITIAL_COEFF\|a_0\|19440` | series_solution_generator.py |
| `INITIAL_EQ` | 2 | `INITIAL_EQ\|C1 + C2\|0` | recurrence_generator.py |
| `INITIAL_SYSTEM` | 2 | `INITIAL_SYSTEM\|C1[1, 1] + C2[1, 0]\|[0, -4]` | ode_system_generator.py |
| `INNER_ANTIDERIV` | 2 | `INNER_ANTIDERIV\|dr\|r^4/4` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_EVAL` | 2, 3 | `INNER_EVAL\|r=0..2\|2^4/4\|4` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_PRODUCT` | 2 | `INNER_PRODUCT\|inner(phi,psi)\|-i` | braket_generator.py |
| `INNER_PRODUCT_SETUP` | 3 | `INNER_PRODUCT_SETUP\|interval=[0,2pi]\|f=sin(4x)\|g=sin(34x)` | function_inner_product_generator.py |
| `INSERT_KEY` | 3 | `INSERT_KEY\|pass 1\|39\|index 1` | algorithm_trace_generator.py |
| `INSERT_PLACE` | 2 | `INSERT_PLACE\|index 1\|24, 39, 25, 28, 36, 38, 32` | algorithm_trace_generator.py |
| `INTEGRAL` | 1, 2 | `INTEGRAL\|integral cos(30x) on [0,2pi]\|0` | fourier_series_generator.py, function_inner_product_generator.py, legendre_construction_generator.py |
| `INTEGRAL_SETUP` | 1 | `INTEGRAL_SETUP\|L = integral from 0 to pi/4 of 3 dtheta` | metric_arc_length_generator.py |
| `INTEGRATE` | 2 | `INTEGRATE\|v_y = u_x\|v=-6xy - 3x + y + phi(x)` | cauchy_riemann_generator.py |
| `INTEGRATION_BY_PARTS` | 2 | `INTEGRATION_BY_PARTS\|u=x\|dv=sin(nx)dx` | fourier_series_generator.py |
| `INTEG_RULE` | 2 | `INTEG_RULE\|trig rule\|∫ cos(u) du = sin(u) + C` | antiderivative_generator.py, definite_integral_generator.py, ode_substitution_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py |
| `INTEG_SETUP` | 2 | `INTEG_SETUP\|∫ -12 cos(4x) dx\|antiderivative` | antiderivative_generator.py, arc_length_generator.py, definite_integral_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, u_substitution_generator.py |
| `INTERCEPT_FORMULA` | 1 | `INTERCEPT_FORMULA\|a = ȳ - b·x̄` | regression_generator.py |
| `INTERFERENCE_FORMULA` | 1 | `INTERFERENCE_FORMULA\|2*n*t=m*lambda` | interference_generator.py |
| `INTERFERENCE_SETUP` | 3 | `INTERFERENCE_SETUP\|thin_film\|m=7, lambda=4\|n=1` | interference_generator.py |
| `INTERP_SETUP` | 3 | `INTERP_SETUP\|newton\|points=(0,-7), (2,-25), (5,-82)\|x=6` | interpolation_generator.py |
| `INTERVAL_CLASS` | 2 | `INTERVAL_CLASS\|s2=-783\|spacelike` | minkowski_interval_generator.py |
| `INT_ABS` | 2 | `INT_ABS\|14\|14` | integer_operations_generator.py |
| `INT_ALIGN` | 2 | `INT_ALIGN\|82320\|65750` | multi_digit_addition_generator.py, multi_digit_subtraction_generator.py |
| `INT_APPLY_SIGN` | 3 | `INT_APPLY_SIGN\|1\|negative\|-1` | integer_operations_generator.py |
| `INT_OP` | 4 | `INT_OP\|+\|10\|2\|12` | integer_operations_generator.py |
| `INT_REWRITE` | 2 | `INT_REWRITE\|10 - (-2)\|10 + 2` | integer_operations_generator.py |
| `INT_SIGN_RULE` | 2 | `INT_SIGN_RULE\|subtract_rule\|Subtracting is adding the opposite` | integer_operations_generator.py |
| `INVARIANT` | 3 | `INVARIANT\|sizes\|3\|4` | structure_isomorphism_generator.py |
| `INVERSE_LAPLACE` | 2 | `INVERSE_LAPLACE\|-1/(s + 4)\|-e^(-4t)` | laplace_ivp_generator.py |
| `INVERSE_MAP` | 2 | `INVERSE_MAP\|x=(u+v)/2\|y=(u-v)/2` | rv_transform_generator.py |
| `INVERSE_METRIC` | 2 | `INVERSE_METRIC\|g^phiphi=1/R^2\|g^thetatheta=1/(R^2 sin^2(phi))` | christoffel_generator.py, riemann_tensor_generator.py |
| `INVERSE_PAIR` | 2 | `INVERSE_PAIR\|(b, 18)\|(18, b)` | function_properties_generator.py, relation_operations_generator.py |
| `INV_FORMULA` | 1 | `INV_FORMULA\|A⁻¹ = (1/det)·[[d, -b], [-c, a]]` | matrix_inverse_generator.py |
| `IRR_SETUP` | 2 | `IRR_SETUP\|c0=-1500,c1=3750\|r0=1/5,iterations=2` | npv_irr_generator.py |
| `IRR_VALUE` | 2 | `IRR_VALUE\|f1\|1625` | npv_irr_generator.py |
| `ITERATE` | 2 | `ITERATE\|n=1\|z=(7/4,4)` | fractal_iteration_generator.py, gradient_descent_generator.py |
| `IVT_SETUP` | 2 | `IVT_SETUP\|f(x) = x^3 + x - 6 on [-3, 1]\|does the IVT guarantee a root?` | mean_value_theorem_generator.py |
| `I_CYCLE` | 2 | `I_CYCLE\|i^3\|-i` | complex_number_ops_generator.py |
| `I_SQUARE` | 2 | `I_SQUARE\|-48i^2\|48` | complex_division_generator.py, complex_log_generator.py, complex_number_ops_generator.py |
| `JACOBIAN` | 2 | `JACOBIAN\|dA\|r dr dtheta` | double_integral_generator.py |
| `JACOBI_END` | 2 | `JACOBI_END\|a=1\|sign 1` | jacobi_symbol_generator.py |
| `JACOBI_RECIPROCITY` | 3 | `JACOBI_RECIPROCITY\|a mod 4 = 1\|n mod 4 = 1\|keep sign` | jacobi_symbol_generator.py |
| `JACOBI_SETUP` | 3 | `JACOBI_SETUP\|a=467\|n=165\|n odd` | jacobi_symbol_generator.py |
| `JACOBI_SWAP` | 3 | `JACOBI_SWAP\|a=165\|n=137\|sign 1` | jacobi_symbol_generator.py |
| `JACOBI_TWO_RULE` | 3 | `JACOBI_TWO_RULE\|n mod 8 = 1\|keep sign\|sign 1` | jacobi_symbol_generator.py |
| `JAC_DET` | 3 | `JAC_DET\|x_u*y_v - x_v*y_u\|3*(-4) - 0*2\|-12` | jacobian_generator.py |
| `JAC_MATRIX` | 2 | `JAC_MATRIX\|[[x_u, x_v], [y_u, y_v]]\|[[3, 0], [2, -4]]` | jacobian_generator.py, rv_transform_generator.py |
| `JAC_SETUP` | 3 | `JAC_SETUP\|x = 3*u\|y = 2*u - 4*v\|d(x,y)/d(u,v)` | jacobian_generator.py |
| `JOINT_SETUP` | 3 | `JOINT_SETUP\|X,Y in {0,1}\|p00=115/1944, p01=155/1944\|p10=155/1944, p11=1519/1944` | joint_distribution_generator.py |
| `KERNEL_BASE` | 3 | `KERNEL_BASE\|A,A\|dot+c=5+1\|6` | feature_map_generator.py, kernel_evaluation_generator.py |
| `KERNEL_EXPONENT` | 2 | `KERNEL_EXPONENT\|A,A\|0` | kernel_evaluation_generator.py |
| `KERNEL_SETUP` | 3 | `KERNEL_SETUP\|type=polynomial\|points=A=(-2,-1), B=(-2,-3), C=(-1,-3)\|c=1,d=3` | kernel_evaluation_generator.py |
| `KERNEL_VALIDITY` | 1 | `KERNEL_VALIDITY\|psd=false` | kernel_validity_generator.py |
| `KERNEL_VALUE` | 2 | `KERNEL_VALUE\|A,A\|216` | feature_map_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py |
| `KIN_FORMULA` | 1 | `KIN_FORMULA\|a = (v_f - v_i)/t` | invariant_mass_generator.py, kinematics_generator.py |
| `KIN_SETUP` | 3, 4 | `KIN_SETUP\|v_i = 7 m/s\|v_f = 25 m/s, t = 6 s\|acceleration` | invariant_mass_generator.py, kinematics_generator.py |
| `KL_FORMULA` | 1 | `KL_FORMULA\|D=sum source_i*log2(source_i/target_i)` | kl_divergence_generator.py |
| `KL_SETUP` | 3 | `KL_SETUP\|P=[1/2,4080/8191,31/16382]\|Q=[1/2,255/16382,3968/8191]\|direction=Q to P` | kl_divergence_generator.py |
| `KMAP_GROUP` | 2 | `KMAP_GROUP\|0110, 0111\|NOT J AND K AND L` | boolean_algebra_generator.py |
| `KMAP_ROW` | 2 | `KMAP_ROW\|JK=00\|0, 0, 0, 0` | boolean_algebra_generator.py |
| `KMAP_SETUP` | 2 | `KMAP_SETUP\|rows JK=00,JK=01,JK=11,JK=10\|columns LM=00,LM=01,LM=11,LM=10` | boolean_algebra_generator.py |
| `KMAP_SIMPLIFY` | 1 | `KMAP_SIMPLIFY\|(NOT J AND K AND L) OR (K AND L AND NOT M) OR (J AND NOT K AND L AND M)` | boolean_algebra_generator.py |
| `KMEANS_SETUP` | 2 | `KMEANS_SETUP\|points=P1=(-2,-1), P2=(-2,4), P3=(3,-2), P4=(1,5)\|centroids=C1=(2,4), C2=(-4,0)` | kmeans_step_generator.py |
| `KNN_DISTANCE` | 3 | `KNN_DISTANCE\|P1\|label=B\|d2=4` | knn_generator.py |
| `KNN_NEIGHBORS` | 1 | `KNN_NEIGHBORS\|P2:2:B,P1:4:B,P5:9:B` | knn_generator.py |
| `KNN_SETUP` | 3 | `KNN_SETUP\|q=(-2,3)\|k=3\|training=P1=(-2,5,B), P2=(-1,2,B), P3=(1,4,A), P4=(-4,-2,A), P5=(-2,0,B)` | knn_generator.py |
| `KNN_SORT` | 1 | `KNN_SORT\|P2:2:B,P1:4:B,P5:9:B,P3:10:A,P4:29:A` | knn_generator.py |
| `KP_EXAMPLE` | 3 | `KP_EXAMPLE\|1\|x=-2,y=-1\|alpha=(0,0,0)` | kernel_perceptron_generator.py |
| `KP_SETUP` | 3 | `KP_SETUP\|kernel=linear\|data=[(-2,-1), (-4,-1), (1,-1)]\|alpha0=(0,0,0)` | kernel_perceptron_generator.py |
| `KP_TERM` | 2 | `KP_TERM\|j=1\|0` | kernel_perceptron_generator.py |
| `KRAFT_CHECK` | 2, 3 | `KRAFT_CHECK\|sum=1\|complete` | huffman_coding_generator.py, kraft_inequality_generator.py |
| `KRAFT_CLASSIFY` | 2 | `KRAFT_CLASSIFY\|slack=1/8\|incomplete` | kraft_inequality_generator.py |
| `KRAFT_FORMULA` | 1 | `KRAFT_FORMULA\|sum 2^-l_i` | huffman_coding_generator.py, kraft_inequality_generator.py |
| `KRAFT_SETUP` | 2 | `KRAFT_SETUP\|A=2, B=1, C=3\|binary prefix code` | kraft_inequality_generator.py |
| `KRAFT_TERM` | 3 | `KRAFT_TERM\|A\|l=2\|1/4` | kraft_inequality_generator.py |
| `KRR_SETUP` | 3 | `KRR_SETUP\|kernel=linear\|data=[(-5,0), (-4,-3)]\|lambda=3,x*=4` | kernel_ridge_generator.py |
| `KV_CACHE` | 2 | `KV_CACHE\|values\|2097152` | flops_memory_generator.py |
| `K_EXPR` | 1, 2 | `K_EXPR\|K = [B]^2/[A]\|4/3 = (2x)^2/(4-x)` | equilibrium_ice_generator.py |
| `L` | 2, 3 | `L\|3\|7\|21` | complement_probability_generator.py, experimental_probability_generator.py, fraction_comparison_generator.py, fraction_op_generator.py, linear_fractional_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `LABEL_COUNT` | 2 | `LABEL_COUNT\|A\|0` | knn_generator.py |
| `LADDER_APPLY` | 2 | `LADDER_APPLY\|a ket18\|sqrt(18) ket17` | ladder_operator_generator.py |
| `LADDER_COMM` | 2 | `LADDER_COMM\|[a,adag] ketn\|ket25` | ladder_operator_generator.py |
| `LADDER_RULE` | 2 | `LADDER_RULE\|J_- = J1_- + J2_-\|lower from highest weights` | clebsch_gordan_generator.py, ladder_operator_generator.py |
| `LADDER_SETUP` | 3 | `LADDER_SETUP\|number_energy\|state=ket18\|hbar=5, omega=1` | ladder_operator_generator.py |
| `LAGRANGE_EQ` | 2 | `LAGRANGE_EQ\|10*x = lambda*2\|x = lambda*2/10` | lagrange_multiplier_generator.py |
| `LAGRANGE_FACTOR` | 3 | `LAGRANGE_FACTOR\|L_0\|j=1\|-9` | interpolation_generator.py |
| `LAGRANGE_SETUP` | 3 | `LAGRANGE_SETUP\|f(x,y) = 5*x^2 + 2*y^2\|constraint 2*x + 5*y = 532\|minimize` | lagrange_multiplier_generator.py |
| `LAGRANGIAN` | 1, 2 | `LAGRANGIAN\|L=T-V` | lagrangian_generator.py |
| `LAG_SETUP` | 3 | `LAG_SETUP\|pendulum\|m=12, L=6\|g=10, q=theta` | lagrangian_generator.py |
| `LAMBDA_SETUP` | 2 | `LAMBDA_SETUP\|((lambda m. (lambda t. ((lambda n. t) t))) (lambda m. m))\|leftmost-outermost` | lambda_reduction_generator.py |
| `LAPLACE` | 2 | `LAPLACE\|L[y' + 4y]\|(sY - 2) + 4Y` | laplace_ivp_generator.py, transfer_function_generator.py |
| `LAPLACE_TABLE` | 1 | `LAPLACE_TABLE\|L{y'} = sY - y(0); L{e^(kt)} = 1/(s-k); L^-1{1/(s-k)} = e^(kt)` | laplace_ivp_generator.py |
| `LATTICE_PAIR` | 3 | `LATTICE_PAIR\|(18, 18)\|lub 18\|glb 18` | partial_order_generator.py |
| `LAURENT_SETUP` | 3 | `LAURENT_SETUP\|center a=-2\|w=(z+2)\|f=(-6 + (z+2) - 3(z+2)^2 - 2(z+2)^3 + (z+2)^4)/(z+2)^2` | laurent_series_generator.py |
| `LAURENT_TERM` | 1 | `LAURENT_TERM\|7(z+3)^-1` | residue_generator.py |
| `LAW` | 3 | `LAW\|Sheffer conjunction\|p ∧ r\|(p ↑ r) ↑ (p ↑ r)` | logical_equivalence_laws_generator.py, set_algebra_laws_generator.py |
| `LAYERNORM_SETUP` | 3 | `LAYERNORM_SETUP\|x=(1,13)\|gamma=(1,2)\|beta=(5,-4)` | layer_norm_generator.py |
| `LB` | 2 | `LB\|{{a}, {a, h, r}}\|{∅, {a}}` | partial_order_generator.py |
| `LCM_FROM_GCD` | 3 | `LCM_FROM_GCD\|90*53\|1\|4770` | lcm_generator.py |
| `LCM_STEP` | 3 | `LCM_STEP\|1\|2\|2` | permutation_group_generator.py, pollard_factorization_generator.py |
| `LEADING_MINOR` | 2 | `LEADING_MINOR\|Delta1\|1` | positive_definite_generator.py |
| `LEAST` | 1 | `LEAST\|none` | induction_verify_generator.py, partial_order_generator.py |
| `LEGENDRE_RESULT` | 3 | `LEGENDRE_RESULT\|40\|-1\|quadratic nonresidue` | quadratic_residue_generator.py |
| `LEGENDRE_SETUP` | 2 | `LEGENDRE_SETUP\|a=3\|p=41` | legendre_construction_generator.py, quadratic_residue_generator.py |
| `LEVEL` | 2 | `LEVEL\|k\|7665` | type_theory_generator.py |
| `LIE_EXP_FORM` | 2 | `LIE_EXP_FORM\|e^(theta J)\|cos(theta)I + sin(theta)J` | lie_exponential_generator.py |
| `LIE_EXP_SETUP` | 4 | `LIE_EXP_SETUP\|SO2\|theta=240 deg\|J=[[0, -1], [1, 0]]\|goal=e^(theta J)` | lie_exponential_generator.py |
| `LIKELIHOOD` | 2 | `LIKELIHOOD\|1/2\|even chance` | likelihood_language_generator.py |
| `LIMITING_REAGENT` | 2 | `LIMITING_REAGENT\|H2\|NH3=12 mol` | stoichiometry_generator.py |
| `LIMIT_CHECK` | 2 | `LIMIT_CHECK\|NH3 from N2=56 mol\|NH3 from H2=12 mol` | stoichiometry_generator.py |
| `LIMIT_SETUP` | 1, 2 | `LIMIT_SETUP\|lim x→3⁺ of abs(x - 3)/(x - 3)\|one-sided: approach from the right` | derivative_limit_def_generator.py, improper_integral_generator.py, lhopital_generator.py, limit_evaluation_generator.py, power_series_generator.py, series_convergence_generator.py |
| `LINEAR_SYSTEM` | 2 | `LINEAR_SYSTEM\|a=1, b=-1/5\|c=0, d=5/6` | markov_chain_generator.py |
| `LINE_EQ` | 1 | `LINE_EQ\|-4y + 16 = 0` | complex_locus_generator.py |
| `LINE_INTEGRAL` | 3 | `LINE_INTEGRAL\|int_0^1 dot dt\|-324/2 + 120\|-42` | line_integral_generator.py |
| `LINE_RELATION_SETUP` | 3 | `LINE_RELATION_SETUP\|perpendicular\|y = -2/3x + 10\|(5, -9)` | parallel_perpendicular_line_generator.py |
| `LINE_SETUP` | 2 | `LINE_SETUP\|F(x,y) = <-3*x + 4*y, 3*x - 3*y>\|from (4, 0) to (-2, 4)` | line_integral_generator.py |
| `LIST_MAX` | 2 | `LIST_MAX\|1/6, 1, 4/3\|4/3` | dedekind_cut_generator.py |
| `LLL_DONE` | 1 | `LLL_DONE\|[(-2,1),(1,3)]` | lll_reduction_generator.py |
| `LLL_SETUP` | 1 | `LLL_SETUP\|[(-3,5),(4,-9)]` | lll_reduction_generator.py |
| `LOCUS_SETUP` | 3 | `LOCUS_SETUP\|z=x+iy\|center=(0,4)\|radius=2` | complex_locus_generator.py |
| `LOG2` | 2 | `LOG2\|1/8\|-3` | entropy_generator.py, huffman_coding_generator.py, mutual_information_generator.py, von_neumann_entropy_generator.py |
| `LOG2_RATIO` | 3 | `LOG2_RATIO\|i=0\|ratio=1\|log=0` | kl_divergence_generator.py |
| `LOG_BOTH_SIDES` | 1 | `LOG_BOTH_SIDES\|ln(e^(2x)) = ln(13)` | exponential_equation_generator.py, log_diff_higher_order_generator.py, separable_ode_generator.py |
| `LOG_EVAL` | 2 | `LOG_EVAL\|20/13\|ln(20/13)` | hyperbolic_distance_generator.py |
| `LOG_EXACT` | 2 | `LOG_EXACT\|log_12(1728)\|3` | master_theorem_generator.py |
| `LOG_FORM` | 1 | `LOG_FORM\|log_b(x) = y ⟺ b^y = x` | log_conversion_generator.py, log_equation_generator.py |
| `LOG_FORMULA` | 1 | `LOG_FORMULA\|log z = ln r + i(arg + 2pi*k)` | complex_log_generator.py |
| `LOG_IDENT` | 2 | `LOG_IDENT\|ln(e) = 1\|1` | exponential_equation_generator.py, log_conversion_generator.py |
| `LOG_LIKELIHOOD` | 1 | `LOG_LIKELIHOOD\|ell(mu)=-(1/(2*5))*sum((x_i-mu)^2)+C` | mle_generator.py |
| `LOG_ONE_TO_ONE` | 1 | `LOG_ONE_TO_ONE\|4x - 1 = x + 5` | log_equation_generator.py |
| `LOG_POWER` | 2 | `LOG_POWER\|log_10(x^2)\|2log_10(x)` | derivative_transcendental_generator.py, log_diff_higher_order_generator.py, log_properties_generator.py, ph_calculation_generator.py |
| `LOG_PRODUCT` | 1, 2 | `LOG_PRODUCT\|log_10(1000x^2)\|log_10(1000) + log_10(x^2)` | log_equation_generator.py, log_properties_generator.py, ph_calculation_generator.py |
| `LOG_QUOTIENT` | 2 | `LOG_QUOTIENT\|log_10(1000x^2/y^3)\|log_10(1000x^2) - log_10(y^3)` | log_properties_generator.py |
| `LOG_SETUP` | 1, 2 | `LOG_SETUP\|log_10(1000x^2/y^3)\|expand` | complex_log_generator.py, log_properties_generator.py |
| `LOG_SOFTMAX` | 2 | `LOG_SOFTMAX\|1\|ln(1/6)` | softmax_gradient_generator.py |
| `LOG_SUPPLIED` | 2 | `LOG_SUPPLIED\|log10(1/10)\|-1` | signal_arithmetic_generator.py |
| `LOG_TERM` | 3 | `LOG_TERM\|22\|ln(2)\|22*ln(2)` | entropy_change_generator.py |
| `LOOKUP_SUPPLIED` | 2 | `LOOKUP_SUPPLIED\|e^(-lambda*t)\|3/13` | named_distribution_generator.py |
| `LORA_COUNT` | 2 | `LORA_COUNT\|r*(d_in+d_out)\|62464` | param_count_generator.py |
| `LOWRANK_SETUP` | 2 | `LOWRANK_SETUP\|A=[[7,0], [0,11]]\|rank=1` | low_rank_approx_generator.py |
| `LP_CORNER_SETUP` | 3 | `LP_CORNER_SETUP\|max z=15x+8y\|0<=x<=21, 0<=y<=18\|x+y<=36` | lp_corner_generator.py |
| `LR_PHASE` | 1 | `LR_PHASE\|decay` | lr_schedule_generator.py |
| `LR_SETUP` | 3 | `LR_SETUP\|base=1/1000\|min=0\|warmup=10,total=210,t=210` | lr_schedule_generator.py |
| `LR_VALUE` | 1 | `LR_VALUE\|0` | lr_schedule_generator.py |
| `LS_LINE` | 2 | `LS_LINE\|a = 5, b = -2\|ŷ = 5 - 2x` | least_squares_generator.py |
| `LS_SETUP` | 2 | `LS_SETUP\|points [(-3, 8), (-1, 10), (1, 6), (3, -4)]\|model y = a + bx` | least_squares_generator.py |
| `LUB` | 1 | `LUB\|{a, h, r}` | partial_order_generator.py |
| `LUHN_DIGIT` | 3 | `LUHN_DIGIT\|digit 7\|double\|14 -> 5` | modular_arithmetic_generator.py |
| `LU_ENTRY` | 3 | `LU_ENTRY\|u11\|a11 = 3\|3` | lu_decomposition_generator.py |
| `LU_RESULT` | 2 | `LU_RESULT\|L\|[[1, 0, 0], [2, 1, 0], [1, -3, 1]]` | lu_decomposition_generator.py |
| `LU_SETUP` | 2 | `LU_SETUP\|A = [[3, 3, -2], [6, 8, -2], [3, -3, -13]]\|unit lower L` | lu_decomposition_generator.py |
| `LZ77_EMIT` | 1 | `LZ77_EMIT\|(0,0,a)` | lz_compression_generator.py |
| `LZ77_EXPAND` | 4 | `LZ77_EXPAND\|(0,0,s)\|no copy\|then add s\|out = s` | lz_compression_generator.py |
| `LZ77_MATCH` | 4 | `LZ77_MATCH\|pos 0\|literal\|offset 0, len 0\|next a` | lz_compression_generator.py |
| `LZ77_SEARCH` | 3 | `LZ77_SEARCH\|pos 1\|start 0\|len 0` | lz_compression_generator.py |
| `LZ78_APPEND` | 2 | `LZ78_APPEND\|empty + r\|out = r` | lz_compression_generator.py |
| `LZ78_DICT` | 2 | `LZ78_DICT\|0\|empty` | lz_compression_generator.py |
| `LZ78_EMIT` | 1 | `LZ78_EMIT\|(0,m)` | lz_compression_generator.py |
| `LZ78_LOOKUP` | 2 | `LZ78_LOOKUP\|index 0\|phrase empty` | lz_compression_generator.py |
| `LZ78_MATCH` | 4 | `LZ78_MATCH\|pos 0\|phrase empty\|index 0\|next m` | lz_compression_generator.py |
| `LZ_SETUP` | 2 | `LZ_SETUP\|LZ77 decode\|(0,0,s), (0,0,x), (2,1,o), (3,1,x), (4,2,$)` | lz_compression_generator.py |
| `M` | 3 | `M\|6\|99\|594` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arc_length_generator.py, arc_sector_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, black_scholes_generator.py, blackbody_generator.py, bond_pricing_generator.py, calorimetry_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_force_generator.py, casimir_generator.py, cayley_table_generator.py, chain_rule_generator.py, channel_capacity_generator.py, christoffel_generator.py, circle_angle_generator.py, classifier_metrics_generator.py, collision_generator.py, commutator_generator.py, complement_probability_generator.py, complex_locus_generator.py, complex_log_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, countability_bijection_generator.py, counterexample_search_generator.py, counting_classics_generator.py, counting_to_probability_generator.py, cramers_rule_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, cyclic_group_generator.py, de_moivre_generator.py, decimal_div_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dimensional_analysis_generator.py, doppler_generator.py, dot_product_generator.py, einstein_summation_generator.py, electrostatics_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equilibrium_ice_generator.py, equivalence_relation_generator.py, error_spotting_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, experimental_probability_generator.py, exponential_model_generator.py, extended_euclid_generator.py, factor_special_forms_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, finite_difference_generator.py, finite_field_generator.py, first_law_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_properties_generator.py, function_table_generator.py, fundamental_form_generator.py, game_theory_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, godel_numbering_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, hawking_generator.py, hermitian_check_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, index_gymnastics_generator.py, index_raising_generator.py, information_gain_generator.py, integers_as_pairs_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kl_divergence_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, long_division_generator.py, lp_corner_generator.py, lr_schedule_generator.py, magnetism_generator.py, markov_chain_generator.py, matrix_calculus_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, mod_exp_generator.py, modular_inverse_generator.py, multi_step_unit_conversion_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, npv_irr_generator.py, ode_system_generator.py, operation_properties_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, ordinal_arithmetic_generator.py, param_count_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, partition_function_generator.py, pca_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_combination_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, planck_units_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, positive_definite_generator.py, primality_test_generator.py, projectile_motion_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rationals_as_pairs_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_solution_generator.py, set_builder_roster_generator.py, set_counting_generator.py, set_operations_generator.py, shm_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simplex_generator.py, solid_revolution_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, stoichiometry_generator.py, svm_margin_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tensor_product_generator.py, tip_bill_split_generator.py, totient_generator.py, transfer_function_generator.py, transformation_generator.py, transient_circuit_generator.py, transportation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, two_sample_test_generator.py, uncertainty_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, unit_conversion_generator.py, vector_ops_generator.py, volume_rect_prism_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py, z_transform_generator.py |
| `MAG_FORMULA` | 1 | `MAG_FORMULA\|magnitude = √(x^2 + y^2)` | magnetism_generator.py, vector_ops_generator.py |
| `MAG_SETUP` | 3 | `MAG_SETUP\|loop_center\|I=26, R=13\|mu0=1` | magnetism_generator.py |
| `MAIN_CONNECTIVE` | 1 | `MAIN_CONNECTIVE\|∨` | wff_parsing_generator.py |
| `MAP` | 2 | `MAP\|b\|f(b) = 18` | function_properties_generator.py |
| `MARGIN` | 2 | `MARGIN\|2/norm(w)\|2/17` | svm_margin_generator.py |
| `MARGINAL` | 1 | `MARGINAL\|P(X=0)=p00+p01` | joint_distribution_generator.py, mutual_information_generator.py |
| `MARKOV_SETUP` | 2, 3 | `MARKOV_SETUP\|two_state\|P00=3/5, P01=2/5\|P10=10/13, P11=3/13` | entropy_rate_markov_generator.py, markov_chain_generator.py |
| `MASTER_CASE` | 2 | `MASTER_CASE\|case 1\|Θ(n^7)` | master_theorem_generator.py |
| `MATMUL_FLOPS` | 2 | `MATMUL_FLOPS\|XW1\|1048576` | flops_memory_generator.py |
| `MATRIX_ADD` | 2 | `MATRIX_ADD\|P0+P1\|[[1,0],[0,1]]` | bch_generator.py, casimir_generator.py, projector_generator.py |
| `MATRIX_ENTRY` | 1 | `MATRIX_ENTRY\|P2_01=P00*P01 + P01*P11` | markov_chain_generator.py |
| `MATRIX_ENTRY_SUM` | 3 | `MATRIX_ENTRY_SUM\|(1,1)\|0 + 0\|0` | gamma_matrix_generator.py |
| `MATRIX_EXP` | 3 | `MATRIX_EXP\|e^A\|I + A\|[[1, 4, 0], [0, 1, 0], [0, 0, 1]]` | bch_generator.py |
| `MATRIX_GROUP_SETUP` | 2 | `MATRIX_GROUP_SETUP\|SL2Z\|M=[[4,3],[-7,-5]]` | matrix_group_check_generator.py |
| `MATRIX_MULT` | 2, 3 | `MATRIX_MULT\|row1 dot col1\|23043240000/23043543601*23043240000/23043543601+83641800/23043543601*83641800/23043543601\|23043240000/23043543601` | projector_generator.py |
| `MATRIX_POWER` | 2 | `MATRIX_POWER\|J^2\|-I` | lie_exponential_generator.py |
| `MATRIX_PRODUCT` | 2 | `MATRIX_PRODUCT\|AB\|[[0, -45i/2], [-45i/2, 0]]` | bch_generator.py, casimir_generator.py, gamma_matrix_generator.py, pauli_algebra_generator.py, structure_constant_generator.py |
| `MATRIX_ROW` | 2 | `MATRIX_ROW\|c\|0 0 0 0` | graph_counting_generator.py, relation_operations_generator.py |
| `MATRIX_SCALE` | 2 | `MATRIX_SCALE\|1/2 ladder sum\|[[3675/242, 0, 0, 0], [0, 8575/242, 0, 0], [0, 0, 8575/242, 0], [0, 0, 0, 3675/242]]` | bch_generator.py, casimir_generator.py |
| `MATRIX_SETUP` | 2 | `MATRIX_SETUP\|hermitian\|A=[[2,0],[0,2]]` | hermitian_check_generator.py |
| `MATRIX_SUB` | 2 | `MATRIX_SUB\|AB - BA\|[[0, 0, -20], [0, 0, 0], [0, 0, 0]]` | bch_generator.py |
| `MATRIX_SUM` | 1 | `MATRIX_SUM\|B=A+A^T` | matrix_calculus_generator.py |
| `MATRIX_VALUE` | 2 | `MATRIX_VALUE\|A\|[[0, -9i/2], [9i/2, 0]]` | pauli_algebra_generator.py, structure_constant_generator.py |
| `MAT_ENTRY` | 2, 3 | `MAT_ENTRY\|(1,1)\|22` | lie_exponential_generator.py, matrix_calculus_generator.py, matrix_ops_generator.py |
| `MAT_SETUP` | 2 | `MAT_SETUP\|A = [[4, 1], [-4, -2]], B = [[5, 4], [2, 5]]\|AB` | determinant_generator.py, diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, row_reduction_generator.py, subspace_basis_generator.py, svd_generator.py |
| `MAX` | 2, 3 | `MAX\|13, 9\|13` | dp_table_generator.py, matrix_norm_generator.py, taxicab_geometry_generator.py |
| `MAXIMAL` | 1 | `MAXIMAL\|{9, 46, 56}` | partial_order_generator.py |
| `MAXTERM` | 2 | `MAXTERM\|011\|B OR NOT C OR NOT D` | boolean_algebra_generator.py |
| `MC_SETUP` | 3 | `MC_SETUP\|expression=x^T A x\|A=[[-4,0], [-4,-4]]\|x=(-5,-4)` | matrix_calculus_generator.py |
| `MEAN` | 1 | `MEAN\|7` | layer_norm_generator.py |
| `MEAN_DIV` | 3 | `MEAN_DIV\|63\|9\|7` | composite_arithmetic_generator.py, five_number_summary_generator.py, regression_generator.py, simple_stats_generator.py, standard_deviation_generator.py |
| `MEASURE` | 3 | `MEASURE\|B\|{d, e, f}\|71/153` | probability_measure_generator.py |
| `MEASURE_BASIS` | 3 | `MEASURE_BASIS\|x\|ket+x=(ket0+ket1)/sqrt(2)\|ket-x=(ket0-ket1)/sqrt(2)` | spin_half_generator.py |
| `MEASURE_FAVORABLE` | 2 | `MEASURE_FAVORABLE\|sector angle\|144` | geometric_probability_generator.py |
| `MEASURE_PROB` | 3 | `MEASURE_PROB\|computational basis\|P(0)=1/2\|P(1)=1/2` | quantum_gate_generator.py |
| `MEASURE_TOTAL` | 2 | `MEASURE_TOTAL\|full circle angle\|360` | geometric_probability_generator.py |
| `MEDIAN_PAIR` | 2 | `MEDIAN_PAIR\|7\|8` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEDIAN_PICK` | 1, 2 | `MEDIAN_PICK\|9` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEMBER` | 1 | `MEMBER\|4/13 ∈ L(√2)` | dedekind_cut_generator.py |
| `MEMBERSHIP_BAD` | 2 | `MEMBERSHIP_BAD\|type(y) = type(y) + 1\|impossible` | type_theory_generator.py |
| `MEMBERSHIP_OK` | 1 | `MEMBERSHIP_OK\|type(m) = type(k) + 1` | type_theory_generator.py |
| `MEMBER_ROW` | 1, 3 | `MEMBER_ROW\|x∈D, x∈H, x∈R` | foundations_critic_generator.py, set_identity_membership_table_generator.py |
| `MEMORY_SETUP` | 3 | `MEMORY_SETUP\|kv_cache\|L=4,h=16,d_k=64\|seq=256,precision_bytes=1` | flops_memory_generator.py |
| `MEMORY_UNIT` | 2 | `MEMORY_UNIT\|MiB\|2` | flops_memory_generator.py |
| `MERGE_BEGIN` | 3 | `MERGE_BEGIN\|merge 1\|lo=0,mid=1,hi=2\|left 31; right 8` | algorithm_trace_generator.py |
| `MERGE_COMPARE` | 3 | `MERGE_COMPARE\|31\|8\|take right` | algorithm_trace_generator.py |
| `MERGE_DONE` | 3 | `MERGE_DONE\|merge 1\|range 0-1\|array 8, 31, 20, 41, 47` | algorithm_trace_generator.py |
| `MERGE_TAKE` | 2 | `MERGE_TAKE\|8\|merged 8` | algorithm_trace_generator.py |
| `METRIC` | 2 | `METRIC\|taxicab vs Chebyshev\|sum of absolute differences vs their max` | taxicab_geometry_generator.py |
| `METRICS_SETUP` | 1 | `METRICS_SETUP\|TP=14, FP=28, FN=23, TN=35` | classifier_metrics_generator.py |
| `METRIC_ARC_SETUP` | 3 | `METRIC_ARC_SETUP\|polar metric\|ds^2=dr^2+r^2 dtheta^2\|r=3, theta:0->pi/4` | metric_arc_length_generator.py |
| `METRIC_FORMULA` | 1 | `METRIC_FORMULA\|precision=TP/(TP+FP)` | classifier_metrics_generator.py |
| `METRIC_RESTRICT` | 2 | `METRIC_RESTRICT\|dr=0\|ds^2=r^2 dtheta^2` | metric_arc_length_generator.py |
| `MGF_SETUP` | 3 | `MGF_SETUP\|P(X=0)=1/6\|P(X=1)=4/9\|P(X=2)=7/18` | mgf_generator.py |
| `MGF_TERM` | 3 | `MGF_TERM\|x=0\|p0*e^(0t)\|1/6` | mgf_generator.py |
| `MIDDLE_EVAL` | 3 | `MIDDLE_EVAL\|r=0..8\|8^2/2\|32` | triple_integral_generator.py |
| `MIDLINE` | 1 | `MIDLINE\|y = -5` | sinusoid_features_generator.py |
| `MIDPOINT` | 2 | `MIDPOINT\|iter 1\|2` | algorithm_trace_generator.py |
| `MID_FORMULA` | 1 | `MID_FORMULA\|M = ((x1 + x2)/2, (y1 + y2)/2)` | circle_equation_generator.py, midpoint_generator.py |
| `MIN` | 2 | `MIN\|49,4\|4` | matrix_norm_generator.py |
| `MIN3` | 4 | `MIN3\|3\|1\|2\|1` | dp_table_generator.py |
| `MINIMAL` | 1 | `MINIMAL\|{6, 9, 30}` | partial_order_generator.py |
| `MINKOWSKI_FORMULA` | 1 | `MINKOWSKI_FORMULA\|eta_total=eta1+eta2` | minkowski_interval_generator.py |
| `MINKOWSKI_SETUP` | 3 | `MINKOWSKI_SETUP\|rapidity_addition\|eta1=4/3\|eta2=-3/2` | minkowski_interval_generator.py |
| `MINTERM` | 2 | `MINTERM\|0001\|NOT J AND NOT K AND NOT L AND M` | boolean_algebra_generator.py |
| `MIN_INITIAL` | 3 | `MIN_INITIAL\|nonaccept A, B\|accept C\|{A,B}, {C}` | dfa_minimization_generator.py |
| `MIN_REFINE` | 2 | `MIN_REFINE\|round 1\|{A}, {B}, {C}` | dfa_minimization_generator.py |
| `MIN_SIGNATURE` | 3 | `MIN_SIGNATURE\|round 1\|A\|0->B0,1->B0` | dfa_minimization_generator.py |
| `MIN_STABLE` | 1 | `MIN_STABLE\|{A}, {B}, {C}` | dfa_minimization_generator.py |
| `MIN_TRANSITION` | 3 | `MIN_TRANSITION\|{A}\|0\|{A}` | dfa_minimization_generator.py |
| `MISSED` | 1 | `MISSED\|1` | function_properties_generator.py |
| `MIX_FORMULA` | 2 | `MIX_FORMULA\|q=(d-b)/(a-b-c+d)\|p=(d-c)/(a-b-c+d)` | game_theory_generator.py |
| `MIX_IMPROPER` | 2 | `MIX_IMPROPER\|2 2/7\|16/7` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `MI_FORMULA` | 1 | `MI_FORMULA\|I=H(X)+H(Y)-H(X,Y)` | mutual_information_generator.py |
| `MI_SETUP` | 2 | `MI_SETUP\|rows=[[0,0,1/8,0,1/8,0];[1/4,0,0,1/4,0,0];[0,1/8,0,0,0,1/8]]\|task=H(X,Y), H(Y given X), and I(X;Y)` | mutual_information_generator.py |
| `MLE_SETUP` | 2, 3 | `MLE_SETUP\|normal_mu\|parameter=mu\|sigma^2=5` | mle_generator.py |
| `MOBIUS_SETUP` | 2 | `MOBIUS_SETUP\|T(z)=(-z + 2)/(-2z - 1)\|z0=-2` | mobius_transform_generator.py |
| `MODE` | 2 | `MODE\|2\|10, 13` | frequency_table_generator.py, simple_stats_generator.py |
| `MODEL` | 1 | `MODEL\|A = P(1 - r)^t` | exponential_model_generator.py |
| `MODEL_APPLY` | 1 | `MODEL_APPLY\|A = 15800 · (1 - 0.7)^2` | exponential_model_generator.py |
| `MODEL_OUTPUT` | 1 | `MODEL_OUTPUT\|-1/2` | activation_generator.py |
| `MODEXP_MULTIPLY` | 2 | `MODEXP_MULTIPLY\|bit 1=1\|43` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODEXP_SETUP` | 3 | `MODEXP_SETUP\|base 43\|exponent 25\|modulus 94` | mod_exp_generator.py |
| `MODEXP_SQUARE` | 2 | `MODEXP_SQUARE\|bit 1=1\|1` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODEXP_STATE` | 2 | `MODEXP_STATE\|after bit 1\|43` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODE_COUNT` | 2 | `MODE_COUNT\|1\|1` | simple_stats_generator.py |
| `MOD_INVERSE` | 2 | `MOD_INVERSE\|43 mod 15\|7` | crt_generator.py, ecdsa_generator.py, elliptic_curve_finite_field_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `MOD_NORMALIZE` | 3 | `MOD_NORMALIZE\|7\|mod 15\|7` | modular_inverse_generator.py, rsa_generator.py |
| `MOD_POWER` | 3 | `MOD_POWER\|55^4\|mod 84\|1` | diffie_hellman_generator.py, pollard_factorization_generator.py, primality_test_generator.py, rsa_generator.py, tonelli_shanks_generator.py, totient_generator.py |
| `MOD_REDUCE` | 3 | `MOD_REDUCE\|6\|mod 12\|6` | calendar_arithmetic_generator.py, cayley_table_generator.py, coset_generator.py, crt_generator.py, cyclic_group_generator.py, de_moivre_generator.py, elliptic_curve_finite_field_generator.py, finite_field_generator.py, jacobi_symbol_generator.py, lie_exponential_generator.py, mod_exp_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, primality_test_generator.py, quadratic_residue_generator.py, reed_solomon_generator.py, rsa_generator.py, totient_generator.py |
| `MOD_SETUP` | 2, 3, 4 | `MOD_SETUP\|12-hour clock\|5 + 1 hours` | modular_arithmetic_generator.py, modular_inverse_generator.py |
| `MOD_SOLVE` | 2 | `MOD_SOLVE\|0 means 12 on a clock\|6 o'clock` | modular_arithmetic_generator.py |
| `MOD_TERM` | 2 | `MOD_TERM\|10 * 7\|70` | modular_arithmetic_generator.py |
| `MOE_FORMULA` | 1 | `MOE_FORMULA\|E = z*·√(p̂(1-p̂)/n)` | confidence_interval_generator.py |
| `MOLAR_MASS` | 2 | `MOLAR_MASS\|CaCO3\|100 g/mol` | gas_stoichiometry_generator.py, stoichiometry_generator.py |
| `MOLAR_VOLUME` | 2 | `MOLAR_VOLUME\|1 mol gas\|24 L` | stoichiometry_generator.py |
| `MOMENT` | 2 | `MOMENT\|m1\|7/10` | adam_step_generator.py |
| `MOMENTUM` | 1 | `MOMENTUM\|p1=m1*u1` | collision_generator.py |
| `MOMENT_X` | 3 | `MOMENT_X\|M_x = 1/2 int y^2 dx\|3^2*17^3/6\|14739/2` | centroid_generator.py |
| `MOMENT_Y` | 3 | `MOMENT_Y\|M_y = int x*y dx\|3*17^3/3\|4913` | centroid_generator.py |
| `MOM_EQUATION` | 2 | `MOM_EQUATION\|E[X]=theta/2\|xbar=theta/2` | method_of_moments_generator.py |
| `MOM_SETUP` | 3 | `MOM_SETUP\|uniform_zero_theta\|parameter=theta\|data=[2,6,16,13,8]` | method_of_moments_generator.py |
| `MONO_ADD_EXP` | 2 | `MONO_ADD_EXP\|x^6 * x^7 = x^(6+7)\|x^13` | monomial_mult_div_generator.py |
| `MONO_DIV_COEFF` | 2 | `MONO_DIV_COEFF\|-9 / 1\|-9` | monomial_mult_div_generator.py |
| `MONO_MULT_COEFF` | 2 | `MONO_MULT_COEFF\|9 * -8\|-72` | monomial_mult_div_generator.py |
| `MONO_SETUP` | 1 | `MONO_SETUP\|(-9x^7) / (x^5)` | monomial_mult_div_generator.py |
| `MONO_SUB_EXP` | 2 | `MONO_SUB_EXP\|x^7 / x^5 = x^(7-5)\|x^2` | monomial_mult_div_generator.py |
| `MOOD` | 2 | `MOOD\|AOA\|figure 3` | syllogism_generator.py |
| `MOVE_TERM` | 2, 3 | `MOVE_TERM\|+5x\|left\|4x+6-5x = -1` | area_between_curves_generator.py, completing_square_generator.py, conic_standard_form_generator.py, linear_complex_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py |
| `MP` | 2 | `MP\|lines 1,2\|(¬m → (a → c)) → (((k → c) ∨ (j → b)) → (((b → m) ∨ e) → ((k → c) ∨ (j → b))))` | hilbert_axiom_derivation_generator.py |
| `MR_DECOMPOSE` | 2 | `MR_DECOMPOSE\|94\|2^1 * 47` | primality_test_generator.py |
| `MR_SETUP` | 2 | `MR_SETUP\|n=95\|witnesses 6, 9` | primality_test_generator.py |
| `MR_SQUARE` | 2 | `MR_SQUARE\|r=1\|15` | primality_test_generator.py |
| `MR_WITNESS` | 1 | `MR_WITNESS\|6` | primality_test_generator.py |
| `MR_WITNESS_RESULT` | 2 | `MR_WITNESS_RESULT\|6\|composite` | primality_test_generator.py |
| `MSE_FORMULA` | 2 | `MSE_FORMULA\|L=(1/n) sum r_i^2\|grad=(2/n) sum r_i*[1,x_i]` | gradient_step_generator.py |
| `MSE_GRADIENT` | 2 | `MSE_GRADIENT\|g0=6\|g1=112/3` | gradient_step_generator.py |
| `MSE_SAMPLE` | 3 | `MSE_SAMPLE\|i=1\|pred=6\|r=16` | gradient_step_generator.py |
| `MSE_SETUP` | 3 | `MSE_SETUP\|model y_hat=w0+w1*x\|samples=[(3,-10), (-1,2), (0,-4)]\|w=(-3,3), eta=1/8` | gradient_step_generator.py |
| `MST_ADD` | 2 | `MST_ADD\|AE\|total 2` | mst_generator.py |
| `MST_SET` | 1 | `MST_SET\|AE` | mst_generator.py |
| `MST_SETUP` | 2 | `MST_SETUP\|weighted undirected graph\|vertices A, B, C, D, E` | mst_generator.py |
| `MU` | 2 | `MU\|-57/34\|round=-2` | lll_reduction_generator.py |
| `MULTIPLY_IF` | 2 | `MULTIPLY_IF\|e^(5x)y' + 5e^(5x)y\|25e^(5x)` | integrating_factor_generator.py, ode_substitution_generator.py |
| `MULTIVALUED_LOG` | 2 | `MULTIVALUED_LOG\|ln(394) + i*(13pi/20 + 2pi*k)\|k in Z` | complex_log_generator.py |
| `MULTI_FORMULA` | 2 | `MULTI_FORMULA\|n!/(a!b!c!...)\|8! / repeats` | stars_and_bars_generator.py |
| `MULTI_SETUP` | 2 | `MULTI_SETUP\|3 V's, 3 I's, 1 N, 1 R\|total 8` | stars_and_bars_generator.py |
| `MUL_PARTIAL` | 3 | `MUL_PARTIAL\|6\|68395\|410370` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_SETUP` | 2 | `MUL_SETUP\|68395\|1956` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_TERM` | 3 | `MUL_TERM\|10\|-7.2x\|-72x` | linear_fractional_generator.py, polynomial_long_division_generator.py, rational_equation_generator.py |
| `MVT_SETUP` | 2 | `MVT_SETUP\|f(x) = x^2 - 5x + 7 on [-1, 5]\|find the c guaranteed by the MVT` | mean_value_theorem_generator.py |
| `MV_CHAIN_SETUP` | 3 | `MV_CHAIN_SETUP\|z = f(x,y) = x^2 + 4*y^2 + 4*x*y - x - y\|x = s + t - 5, y = -2*s - t + 3\|(s,t) = (-1, 2)` | multivar_chain_rule_generator.py |
| `NATURAL_SETUP` | 3 | `NATURAL_SETUP\|energy\|hbar=1,c=1\|E=3 eV` | natural_units_generator.py |
| `NB_FEATURE_COUNT` | 3 | `NB_FEATURE_COUNT\|Spam\|long=1\|count=16` | naive_bayes_generator.py |
| `NB_LIKELIHOOD` | 3 | `NB_LIKELIHOOD\|Spam\|long=1\|17/22` | naive_bayes_generator.py |
| `NB_PRIOR` | 2 | `NB_PRIOR\|Spam\|1/2` | naive_bayes_generator.py |
| `NB_SCORE` | 2 | `NB_SCORE\|Spam\|start=1/2` | naive_bayes_generator.py |
| `NB_SETUP` | 3 | `NB_SETUP\|query=long=1, link=0\|alpha=1\|classes=Spam,Ham` | naive_bayes_generator.py |
| `NCR` | 2 | `NCR\|C(3,2)\|3` | binomial_probability_generator.py, derangement_generator.py, generating_function_generator.py, hypercube_counting_generator.py |
| `NEAREST` | 2 | `NEAREST\|queen\|(-7,-4)` | embedding_similarity_generator.py |
| `NEED` | 2 | `NEED\|line 1 converts 15% to 0.15\|line 3 adds the tip 7.35 to the bill` | fill_in_step_generator.py |
| `NEGATE` | 2 | `NEGATE\|602\|-602` | countability_bijection_generator.py |
| `NEG_CONNECTIVE` | 2 | `NEG_CONNECTIVE\|¬(Prime(n) → Odd(n))\|Prime(n) ∧ ¬Odd(n)` | prenex_normal_form_generator.py, quantifier_negation_generator.py |
| `NEG_LOG` | 2 | `NEG_LOG\|p=1/64\|ln(64)` | perplexity_generator.py |
| `NEG_QUANT` | 2 | `NEG_QUANT\|¬∀n\|∃n ¬` | prenex_normal_form_generator.py, quantifier_negation_generator.py |
| `NEST` | 2 | `NEST\|{a}\|{{{∅}, {∅, {∅}}, {{∅, {∅}}}, {{{{∅}}}}}}` | hereditarily_finite_set_generator.py |
| `NET_SETUP` | 2 | `NET_SETUP\|2 right triangles with legs 3 and 4; rectangles 3 by 11, 4 by 11, and 5 by 11\|total surface area` | nets_surface_area_generator.py |
| `NEWTON_DD` | 2 | `NEWTON_DD\|f[x0,x1]\|-9` | interpolation_generator.py |
| `NEWTON_SETUP` | 2, 3 | `NEWTON_SETUP\|f(x)=x^2-59\|f'(x)=2x\|x0=8,iterations=2` | newton_raphson_generator.py, newtons_laws_generator.py |
| `NEWTON_STEP` | 2 | `NEWTON_STEP\|1\|103/125` | npv_irr_generator.py |
| `NEWTON_UPDATE` | 3 | `NEWTON_UPDATE\|1\|x_0=8\|x_1=123/16` | newton_raphson_generator.py |
| `NEW_SLOPE` | 2 | `NEW_SLOPE\|New slope (m2) = 3/2\|Perpendicular lines have negative reciprocal slopes` | parallel_perpendicular_line_generator.py |
| `NEW_STRING` | 1 | `NEW_STRING\|011100` | cantor_diagonal_generator.py |
| `NFA_ACCEPT` | 1 | `NFA_ACCEPT\|p2` | nfa_simulation_generator.py |
| `NFA_ACTIVE` | 2 | `NFA_ACTIVE\|start\|{p1}` | nfa_simulation_generator.py |
| `NFA_EPSILON` | 2 | `NFA_EPSILON\|r0\|{r7}` | nfa_simulation_generator.py |
| `NFA_INPUT` | 1 | `NFA_INPUT\|bbabba` | nfa_simulation_generator.py |
| `NFA_MOVE` | 4 | `NFA_MOVE\|{p1}\|b\|p1->{p4}\|{p4}` | nfa_simulation_generator.py |
| `NFA_READ` | 2 | `NFA_READ\|pos 1\|b` | nfa_simulation_generator.py |
| `NFA_SETUP` | 3 | `NFA_SETUP\|states p1, p2, p4, p7\|alphabet a, b\|start p1` | nfa_simulation_generator.py |
| `NFA_TRANSITION` | 3 | `NFA_TRANSITION\|p1\|a\|{p7}` | nfa_simulation_generator.py |
| `NILPOTENT` | 3 | `NILPOTENT\|theta^2=0\|-48theta^2\|0` | grassmann_generator.py |
| `NLL` | 2 | `NLL\|131 tokens\|131*ln(64)` | perplexity_generator.py |
| `NORM2` | 2 | `NORM2\|b1\|34` | lll_reduction_generator.py |
| `NORMALIZE` | 2 | `NORMALIZE\|2/3 + 1/3\|1` | clebsch_gordan_generator.py, layer_norm_generator.py |
| `NORMALIZE_SIGN` | 2 | `NORMALIZE_SIGN\|(-2,1)\|(2,-1)` | lll_reduction_generator.py |
| `NORMAL_EQ` | 2 | `NORMAL_EQ\|X^T X\|[[4, 0], [0, 20]]` | least_squares_generator.py |
| `NORMAL_SLOPE` | 2 | `NORMAL_SLOPE\|-1/(-6)\|1/6` | tangent_line_generator.py |
| `NORMAL_SYMMETRY` | 2 | `NORMAL_SYMMETRY\|N_neg_d1=0.35\|N_neg_d2=0.4` | black_scholes_generator.py |
| `NORM_CHECK` | 2 | `NORM_CHECK\|P(+x)+P(-x)\|1` | spin_half_generator.py |
| `NORM_SETUP` | 2 | `NORM_SETUP\|X ~ N(63, 25)\|raw value for z = -1.04` | matrix_norm_generator.py, normal_table_generator.py, z_score_generator.py |
| `NORM_SQUARED` | 2 | `NORM_SQUARED\|p\|18` | quaternion_generator.py |
| `NO_COLLISION` | 1 | `NO_COLLISION\|all outputs distinct` | function_properties_generator.py |
| `NO_MISSED` | 1 | `NO_MISSED\|all codomain values hit` | function_properties_generator.py |
| `NO_REDEX` | 2 | `NO_REDEX\|lambda t. t\|no beta redex remains` | lambda_reduction_generator.py |
| `NO_WITNESS` | 2, 3 | `NO_WITNESS\|x=30\|tried y in {5, 10, 19, 23, 30}` | peano_arithmetic_generator.py, quantifier_finite_domain_generator.py |
| `NPV_SETUP` | 2 | `NPV_SETUP\|c0=-1900,c1=1400,c2=1000,c3=1100\|rate=5%` | npv_irr_generator.py |
| `NPV_TERM` | 2 | `NPV_TERM\|t=0\|-1900` | npv_irr_generator.py |
| `NULL_REL` | 2 | `NULL_REL\|x1 - 2*x3 + x4 = 0\|x1 = 2*x3 - x4` | subspace_basis_generator.py |
| `NULL_VECTOR` | 2 | `NULL_VECTOR\|x3=1, x4=0\|[2, -1, 1, 0]` | subspace_basis_generator.py |
| `NUMBER_OPERATOR` | 2 | `NUMBER_OPERATOR\|N ket18\|18 ket18` | ladder_operator_generator.py |
| `NW_ALLOC` | 1, 3 | `NW_ALLOC\|cell x11\|min(19,16)\|16` | transportation_generator.py |
| `NYQUIST` | 1 | `NYQUIST\|required rate = 2*f_max` | signal_arithmetic_generator.py |
| `OBJECTIVE` | 1 | `OBJECTIVE\|at (0,0)` | lp_corner_generator.py |
| `OCCURS_CHECK` | 3 | `OCCURS_CHECK\|X\|f(X)\|fail` | unification_generator.py |
| `ODDS` | 2 | `ODDS\|for complement\|1:102` | odds_probability_generator.py |
| `ODDS_FORMULA` | 1 | `ODDS_FORMULA\|odds for Aᶜ = P(Aᶜ) : P(A)` | odds_probability_generator.py |
| `ODDS_REDUCE` | 2 | `ODDS_REDUCE\|856:174\|428:87` | odds_probability_generator.py |
| `ODD_VERTICES` | 2 | `ODD_VERTICES\|C, E\|2` | euler_circuit_generator.py |
| `ODE_SETUP` | 2, 3 | `ODE_SETUP\|dy/dt = ky; y doubles every 212 hours\|find k exactly` | euler_method_generator.py, exact_ode_generator.py, integrating_factor_generator.py, laplace_ivp_generator.py, logistic_growth_generator.py, ode_substitution_generator.py, ode_system_generator.py, runge_kutta_generator.py, second_order_ode_generator.py, separable_ode_generator.py, series_solution_generator.py, stability_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `OPTICS_FORMULA` | 1 | `OPTICS_FORMULA\|1/f=1/d_o+1/d_i` | optics_generator.py |
| `OPTICS_SETUP` | 3 | `OPTICS_SETUP\|mirror_magnification\|f=22, d_o=47\|h_o=2` | optics_generator.py |
| `OPT_SETUP` | 2 | `OPT_SETUP\|x + y = 1449, x, y > 0\|maximize P = x·y^2` | optimization_generator.py |
| `ORBIT_FORMULA` | 1 | `ORBIT_FORMULA\|F=G*m1*m2/r^2` | orbital_mechanics_generator.py |
| `ORBIT_SETUP` | 3 | `ORBIT_SETUP\|gravity_force\|m1=15, m2=33\|r=20, G=1` | orbital_mechanics_generator.py |
| `ORDER_PAIR` | 2 | `ORDER_PAIR\|2 ≤ 27\|reachable in H` | partial_order_generator.py |
| `ORDER_PDF` | 1 | `ORDER_PDF\|f_{1:6}(x)=6*(1-x)^5` | order_statistics_generator.py |
| `ORDER_SETUP` | 3 | `ORDER_SETUP\|n=6\|k=1\|q=1/6` | order_statistics_generator.py |
| `ORDER_START` | 2 | `ORDER_START\|8\|identity 0` | cayley_table_generator.py |
| `ORDER_STEP` | 2 | `ORDER_STEP\|k=1\|8` | cayley_table_generator.py |
| `ORD_CMP` | 2 | `ORD_CMP\|coefficients at exponent 3\|4 > 3` | ordinal_arithmetic_generator.py |
| `ORD_RULE` | 2, 3 | `ORD_RULE\|normalization\|expand the finite right factor` | ordinal_arithmetic_generator.py |
| `ORTHOGONALITY` | 2 | `ORTHOGONALITY\|lower multiplet\|orthogonal to higher J` | clebsch_gordan_generator.py |
| `OR_SETUP` | 3 | `OR_SETUP\|EOQ\|D=350\|S=25, H=7` | or_formula_generator.py |
| `OUTCOME_CHECK` | 3 | `OUTCOME_CHECK\|17\|the two-digit number is greater than 81\|no` | sample_space_list_generator.py |
| `OUTER_ANTIDERIV` | 2 | `OUTER_ANTIDERIV\|dx\|15*x^2 + 35*x` | double_integral_generator.py |
| `OUTER_EVAL` | 3 | `OUTER_EVAL\|y=0..10\|4*2*5^2/2\|100` | double_integral_generator.py |
| `OUTER_PRODUCT` | 1 | `OUTER_PRODUCT\|rho=1/2(ket00bra00+e^(-i143π/90)ket00bra11+e^(i143π/90)ket11bra00+ket11bra11)` | partial_trace_generator.py |
| `OUTPUT` | 1 | `OUTPUT\|y_hat=-15` | backprop_generator.py |
| `PAIR` | 2 | `PAIR\|apricot\|badger` | one_to_one_correspondence_generator.py |
| `PAIRING` | 2 | `PAIRING\|(42, 86)\|(m + n)(m + n + 1)/2 + n` | cantor_pairing_generator.py |
| `PAIR_RULE` | 1, 2 | `PAIR_RULE\|subtract min(a, b) from both coordinates` | integers_as_pairs_generator.py, rationals_as_pairs_generator.py |
| `PARALLEL_RELATION` | 1 | `PARALLEL_RELATION\|2x + 15 = 5x - 12` | angle_relationships_generator.py |
| `PARALLEL_SETUP` | 2 | `PARALLEL_SETUP\|alternate_interior\|Alternate interior angles are equal` | angle_relationships_generator.py |
| `PARALLEL_SOLVE` | 2 | `PARALLEL_SOLVE\|-3x = -27\|x = 9` | angle_relationships_generator.py |
| `PARAMS` | 3 | `PARAMS\|W1=[[-1,-1], [2,2]]\|b1=(1,-1)\|v=(-2,-2), c=-1` | backprop_generator.py |
| `PARAM_PART` | 2 | `PARAM_PART\|attention_per_layer\|11943936` | param_count_generator.py |
| `PARAM_PATH` | 3 | `PARAM_PATH\|r(t)\|(-6*t + 4, 4*t)\|0 <= t <= 1` | line_integral_generator.py |
| `PARAM_SETUP` | 2, 3 | `PARAM_SETUP\|x = 4t + 14, y = 9t + 5\|eliminate t` | param_count_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py |
| `PARITY` | 1, 2 | `PARITY\|transpositions 3\|odd` | fourier_series_generator.py, permutation_group_generator.py |
| `PARITY_CALC` | 2 | `PARITY_CALC\|p1=d1 xor d2 xor d4\|1 xor 0 xor 0=1` | hamming_code_generator.py |
| `PARSE` | 2, 3 | `PARSE\|p\|atom` | wff_parsing_generator.py |
| `PARTFRAC_SETUP` | 1 | `PARTFRAC_SETUP\|(-x - 8)/((x - 1)(x + 2)) = A/(x - 1) + B/(x + 2)` | partial_fractions_generator.py, telescoping_generator.py |
| `PARTIAL` | 2 | `PARTIAL\|u_x\|-2x + 5` | cauchy_riemann_generator.py, fundamental_form_generator.py, hamiltonian_generator.py, lagrangian_generator.py |
| `PARTIAL_FRAC` | 2 | `PARTIAL_FRAC\|Y(s)\|-1/(s + 4) + 3/(s - 1)` | laplace_ivp_generator.py |
| `PARTIAL_RESULT` | 2 | `PARTIAL_RESULT\|f_x\|16*x^3*y^4 + 18*x^2*y^2` | div_curl_generator.py, exact_ode_generator.py, gradient_generator.py, hessian_classify_generator.py, jacobian_generator.py, lagrange_multiplier_generator.py, line_integral_generator.py, multivar_chain_rule_generator.py, partial_derivative_generator.py, vector_theorem_generator.py |
| `PARTIAL_RULE` | 3 | `PARTIAL_RULE\|4*x^4*y^4\|d/dx\|16*x^3*y^4` | partial_derivative_generator.py |
| `PARTIAL_SETUP` | 2 | `PARTIAL_SETUP\|f(x,y) = 4*x^4*y^4 + 6*x^3*y^2\|f_xx` | partial_derivative_generator.py |
| `PARTIAL_TRACE` | 2 | `PARTIAL_TRACE\|ket00bra00\|ket0bra0` | partial_trace_generator.py |
| `PARTICLE_TABLE` | 1 | `PARTICLE_TABLE\|pi+(Q=1,B=0,Le=0,Lmu=0); nu_mu(Q=0,B=0,Le=0,Lmu=1); mu+(Q=1,B=0,Le=0,Lmu=-1); pi0(Q=0,B=0,Le=0,Lmu=0)` | conservation_law_generator.py |
| `PARTICULAR` | 2 | `PARTICULAR\|y_p\|-3e^(2x)` | undetermined_coeff_generator.py, variation_parameters_generator.py |
| `PARTICULAR_CHECK` | 2 | `PARTICULAR_CHECK\|K = -1\|-5K - 6K - 12 = K` | recurrence_generator.py |
| `PARTICULAR_TRY` | 2 | `PARTICULAR_TRY\|a_n = K\|constant forcing` | recurrence_generator.py |
| `PARTITION` | 1 | `PARTITION\|{{22}, {24}, {35, 71}, {47, 65}, {48}, {49, 58}, {70}, {81}, {87}}` | equivalence_relation_generator.py |
| `PARTITION_FORMULA` | 1 | `PARTITION_FORMULA\|Z=g0+g1*b` | partition_function_generator.py |
| `PARTITION_SETUP` | 3 | `PARTITION_SETUP\|two_level\|g0=1, g1=1\|epsilon=6, b=1/3` | partition_function_generator.py |
| `PARTS_CHOOSE` | 2 | `PARTS_CHOOSE\|u = -65x, dv = e^x dx\|du = -65 dx, v = e^x` | integration_by_parts_generator.py |
| `PARTS_FORMULA` | 1 | `PARTS_FORMULA\|∫ u dv = uv - ∫ v du` | integration_by_parts_generator.py |
| `PASCAL_ROW` | 2 | `PASCAL_ROW\|0\|1` | pascal_triangle_generator.py |
| `PASCAL_SETUP` | 1 | `PASCAL_SETUP\|row 5` | pascal_triangle_generator.py |
| `PATH` | 2 | `PATH\|25→27→25\|add (25, 25)` | relation_closure_generator.py |
| `PATH_DERIV` | 2 | `PATH_DERIV\|r'(t)\|(-6, 4)` | curve_geometry_generator.py, line_integral_generator.py |
| `PAULI_IDENTITY` | 3 | `PAULI_IDENTITY\|sigma_y sigma_y\|delta_ij I\|I` | pauli_algebra_generator.py |
| `PAULI_MATRIX` | 2 | `PAULI_MATRIX\|sigma_z\|[[1,0],[0,-1]]` | spin_half_generator.py |
| `PAULI_SETUP` | 3 | `PAULI_SETUP\|product\|A=-sigma_y\|B=-sigma_y` | pauli_algebra_generator.py |
| `PCA_SETUP` | 2 | `PCA_SETUP\|points=[(8,1), (-8,1), (0,2), (0,0)]\|population covariance` | pca_generator.py |
| `PC_VECTOR` | 2 | `PC_VECTOR\|e1\|(1,0)` | pca_generator.py |
| `PDA_POP` | 2 | `PDA_POP\|A\|stack=$A` | pda_simulation_generator.py |
| `PDA_PUSH` | 2 | `PDA_PUSH\|A\|stack=$A` | pda_simulation_generator.py |
| `PDA_READ` | 1 | `PDA_READ\|a` | pda_simulation_generator.py |
| `PDA_REJECT` | 1 | `PDA_REJECT\|too many b symbols` | pda_simulation_generator.py |
| `PDA_SETUP` | 2 | `PDA_SETUP\|a^n b^n\|stack=$` | pda_simulation_generator.py |
| `PDA_STATE` | 3 | `PDA_STATE\|pos 1\|push\|stack=$` | pda_simulation_generator.py |
| `PDE_SETUP` | 2 | `PDE_SETUP\|u_tt = 64u_xx\|u(x,0)=x^2, u_t(x,0)=0` | separable_pde_generator.py |
| `PDF_FORMULA` | 1 | `PDF_FORMULA\|f_Y(y)=1/(42*sqrt(y))` | rv_transform_generator.py |
| `PD_SETUP` | 2 | `PD_SETUP\|A=[[1,3], [3,-4]]\|Sylvester criterion` | positive_definite_generator.py |
| `PEANO_BASE` | 2 | `PEANO_BASE\|SSSSSS0 ∸ 0\|SSSSSS0` | peano_arithmetic_generator.py |
| `PEANO_EQ` | 2 | `PEANO_EQ\|SSSSSS0 ∸ SSS0\|pred(SSSSSS0 ∸ SS0)` | peano_arithmetic_generator.py |
| `PERCENT_CALC_PART` | 3 | `PERCENT_CALC_PART\|1.3\|1950\|2535` | percent_problem_generator.py |
| `PERCENT_TO_DEC` | 2 | `PERCENT_TO_DEC\|87%\|0.87` | annuity_generator.py, bond_pricing_generator.py, composite_arithmetic_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finance_generator.py, fraction_decimal_percent_converter.py, npv_irr_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, portfolio_generator.py, tip_bill_split_generator.py |
| `PERCEPTRON_RULE` | 2 | `PERCEPTRON_RULE\|score=w0+w1*x1+w2*x2\|if y*score <= 0 update` | perceptron_generator.py |
| `PERCEPTRON_SAMPLE` | 3 | `PERCEPTRON_SAMPLE\|i=1\|x=(0,1)\|y=-1` | perceptron_generator.py |
| `PERCEPTRON_SCORE` | 2 | `PERCEPTRON_SCORE\|i=1\|score=-2` | perceptron_generator.py |
| `PERCEPTRON_SETUP` | 3 | `PERCEPTRON_SETUP\|eta=1\|w=(-2,-2,0)\|samples=[(0,1,-1), (1,-2,1), (1,-3,1)]` | perceptron_generator.py |
| `PERCEPTRON_UPDATE` | 2, 3 | `PERCEPTRON_UPDATE\|i=1\|no change\|w=(-2,-2,0)` | perceptron_generator.py |
| `PERIM` | 1 | `PERIM\|42` | geometry_area_perimeter_generator.py, polygon_perimeter_generator.py |
| `PERIOD` | 1 | `PERIOD\|60°` | sinusoid_features_generator.py |
| `PERM_COMPOSE` | 3 | `PERM_COMPOSE\|i=1\|tau(i)=5\|sigma(tau(i))=2` | permutation_group_generator.py |
| `PERM_FORMULA` | 1 | `PERM_FORMULA\|P(n, r) = n·(n-1)···(n-r+1), 7 factors` | permutation_combination_generator.py |
| `PERM_RESULT` | 1 | `PERM_RESULT\|[2, 4, 5, 1, 3, 6]` | permutation_group_generator.py |
| `PERM_SETUP` | 2, 3 | `PERM_SETUP\|P(18, 7)\|n!/(n-r)!` | permutation_combination_generator.py, permutation_group_generator.py |
| `PERPLEXITY` | 2 | `PERPLEXITY\|exp(CE)\|64` | perplexity_generator.py |
| `PERPLEXITY_SETUP` | 2 | `PERPLEXITY_SETUP\|tokens=131\|p=1/64` | perplexity_generator.py |
| `PE_ENTRY` | 2 | `PE_ENTRY\|0\|-1` | positional_encoding_generator.py |
| `PE_SETUP` | 3 | `PE_SETUP\|position=112\|d=2\|theta=3pi/2` | positional_encoding_generator.py |
| `PF_PRIME` | 1 | `PF_PRIME\|347` | godel_numbering_generator.py, prime_factorization_generator.py, repeating_decimal_generator.py |
| `PF_STEP` | 3 | `PF_STEP\|1041\|3\|347` | godel_numbering_generator.py, prime_factorization_generator.py, repeating_decimal_generator.py |
| `PHASE_SHIFT` | 1 | `PHASE_SHIFT\|45° right` | sinusoid_features_generator.py |
| `PHI_STEP` | 2 | `PHI_STEP\|p=29\|28` | totient_generator.py |
| `PHYS_FORMULA` | 1 | `PHYS_FORMULA\|F = W/d` | physics_formula_generator.py |
| `PHYS_SETUP` | 3 | `PHYS_SETUP\|W = 1224 joules\|d = 18 meters\|force` | physics_formula_generator.py |
| `PH_FORMULA` | 1 | `PH_FORMULA\|pOH=-log10([OH-]), pH=14-pOH` | ph_calculation_generator.py |
| `PH_SETUP` | 2, 3 | `PH_SETUP\|hydroxide_with_log\|[OH-]=4*10^-12\|log10(4)=0.6` | ph_calculation_generator.py |
| `PI2_NUM` | 3 | `PI2_NUM\|-7/768\|π^2\|-7π^2/768` | casimir_force_generator.py |
| `PICTO_COUNT` | 2 | `PICTO_COUNT\|Buses\|8` | graph_interpret_generator.py |
| `PICTO_KEY` | 2 | `PICTO_KEY\|★\|10` | graph_interpret_generator.py |
| `PIVOT` | 3 | `PIVOT\|row=s1\|column=x\|pivot=1` | simplex_generator.py |
| `PIVOT_COLS` | 2 | `PIVOT_COLS\|columns 1, 2\|rank = 2` | subspace_basis_generator.py |
| `PI_COEFF` | 2 | `PI_COEFF\|3π/10\|3/10` | arc_sector_generator.py |
| `PI_DEN` | 3 | `PI_DEN\|1/56\|π\|1/(56π)` | gauss_law_generator.py, hawking_generator.py, magnetism_generator.py |
| `PI_MULT` | 3 | `PI_MULT\|2/3\|π\|2π/3` | shm_generator.py |
| `PLACE_DP` | 3 | `PLACE_DP\|2262\|2\|22.62` | decimal_mult_generator.py |
| `PLACE_DP_Q` | 3 | `PLACE_DP_Q\|165\|3\|165` | decimal_div_generator.py, percent_problem_generator.py |
| `PLACE_VALUE` | 2 | `PLACE_VALUE\|D * 16^0\|13` | base_conversion_generator.py |
| `PLANCK_SETUP` | 4 | `PLANCK_SETUP\|mass\|hbar=4\|G=4\|c=25` | planck_units_generator.py |
| `PLUS_MINUS` | 2 | `PLUS_MINUS\|x + 79 = ±53\|x + 79 = 53 or x + 79 = -53` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `POINT_FROM_LAMBDA` | 3 | `POINT_FROM_LAMBDA\|x\|80*2/10\|16` | lagrange_multiplier_generator.py |
| `POINT_SLOPE_SETUP` | 1 | `POINT_SLOPE_SETUP\|y - 9 = 0(x + 8)` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py |
| `POLAR_AREA_FORMULA` | 1 | `POLAR_AREA_FORMULA\|A = (1/2) ∫ r^2 dθ` | parametric_calculus_generator.py |
| `POLAR_BOUNDS` | 2 | `POLAR_BOUNDS\|r\|0..2` | double_integral_generator.py |
| `POLAR_CONVERT` | 2 | `POLAR_CONVERT\|x^2 + y^2\|r^2` | double_integral_generator.py |
| `POLAR_EVAL` | 3 | `POLAR_EVAL\|theta range * radial integral\|pi * 4\|4*pi` | double_integral_generator.py |
| `POLAR_FORM` | 1 | `POLAR_FORM\|11 cis(270 deg)` | euler_formula_generator.py |
| `POLAR_FORMULA` | 1 | `POLAR_FORMULA\|x = r cos θ, y = r sin θ` | polar_parametric_generator.py |
| `POLAR_SETUP` | 2, 3 | `POLAR_SETUP\|r = 16 cos θ\|pole=(-15, 11)\|rectangular equation` | parametric_calculus_generator.py, polar_parametric_generator.py |
| `POLES` | 1 | `POLES\|s=-5, -9` | transfer_function_generator.py |
| `POLE_ORDER` | 1 | `POLE_ORDER\|1` | residue_generator.py |
| `POLE_TEST` | 3 | `POLE_TEST\|pole 7\|abs(7) < 7\|outside` | contour_integral_generator.py |
| `POLISH` | 1 | `POLISH\|CKArpKqpr` | wff_parsing_generator.py |
| `POLLARD_FACTOR` | 2 | `POLLARD_FACTOR\|7\|13` | pollard_factorization_generator.py |
| `POLLARD_PM1_SETUP` | 3 | `POLLARD_PM1_SETUP\|n=589\|base=2\|B=5` | pollard_factorization_generator.py |
| `POLLARD_RHO_SETUP` | 3 | `POLLARD_RHO_SETUP\|n=91\|c=3\|x0=8` | pollard_factorization_generator.py |
| `POLYDIV_SETUP` | 2 | `POLYDIV_SETUP\|x^3 - x^2 - 13x + 11\|x - 4` | finite_field_generator.py, polynomial_long_division_generator.py |
| `POLY_ACCUM` | 2 | `POLY_ACCUM\|x^0\|2` | finite_field_generator.py |
| `POLY_ADD_START` | 1 | `POLY_ADD_START\|max degree 1` | finite_field_generator.py |
| `POLY_COEFF` | 3 | `POLY_COEFF\|sum\|x^0\|3` | finite_field_generator.py |
| `POLY_COMBINE` | 1 | `POLY_COMBINE\|-3x^2 + 6x - 5` | multiplying_binomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_DIST_NEG` | 1 | `POLY_DIST_NEG\|Distribute negative sign to second polynomial` | polynomial_add_sub_generator.py |
| `POLY_DIV_SETUP` | 1 | `POLY_DIV_SETUP\|(-36x^7 + 18x^6) / (9x^3)` | polynomial_div_monomial_generator.py |
| `POLY_DIV_SPLIT` | 1 | `POLY_DIV_SPLIT\|(-36x^7) / (9x^3) + (18x^6) / (9x^3)` | polynomial_div_monomial_generator.py |
| `POLY_FORMULA` | 1 | `POLY_FORMULA\|A = (1/2)·a·P` | regular_polygon_area_generator.py |
| `POLY_GROUP_LIKE` | 1 | `POLY_GROUP_LIKE\|(3x^2 -6x^2) + (6x) + (-8 +3)` | multiplying_polynomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_INPUT` | 2 | `POLY_INPUT\|f(x)\|2x + 1` | finite_field_generator.py |
| `POLY_MULT_SETUP` | 1 | `POLY_MULT_SETUP\|(2x + 3)(-2x^2 - 3x - 3)` | multiplying_polynomials_generator.py |
| `POLY_MUL_START` | 2 | `POLY_MUL_START\|degree 1\|degree 1` | finite_field_generator.py |
| `POLY_REMAINDER` | 1 | `POLY_REMAINDER\|x^4 + x^3` | finite_field_generator.py |
| `POLY_SCALE` | 3 | `POLY_SCALE\|x^3 - 3x/5\|5/2\|(5x^3 - 3x)/2` | legendre_construction_generator.py |
| `POLY_SETUP` | 1, 2 | `POLY_SETUP\|(3x^2 - 8) + (-6x^2 + 6x + 3)` | factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, polynomial_add_sub_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, regular_polygon_area_generator.py |
| `POLY_SUB` | 2, 3 | `POLY_SUB\|(x^3 - x^2) - (x^3 - 4x^2)\|3x^2` | legendre_construction_generator.py, polynomial_long_division_generator.py |
| `PORT_FORMULA` | 2 | `PORT_FORMULA\|E=wA*rA+wB*rB\|Var=wA^2*varA+wB^2*varB+2*wA*wB*cov` | portfolio_generator.py |
| `PORT_RESULT` | 2 | `PORT_RESULT\|expected_return=0.086\|variance=0.0424` | portfolio_generator.py |
| `PORT_SETUP` | 3 | `PORT_SETUP\|wA=0.4,wB=0.6\|rA=8%,rB=9%\|varA=0.0625,varB=0.09,cov=0` | portfolio_generator.py |
| `POSTERIOR_PARAM` | 1 | `POSTERIOR_PARAM\|alpha' = alpha + successes` | bayesian_update_generator.py |
| `POST_PRECISION` | 1 | `POST_PRECISION\|prior precision + data precision` | bayesian_update_generator.py |
| `POTENTIAL_BUILD` | 3 | `POTENTIAL_BUILD\|integrate P dx\|4*x^2 - x*y + 4*x + g(y)\|g'(y) remains` | exact_ode_generator.py, line_integral_generator.py |
| `POTENTIAL_RESULT` | 2 | `POTENTIAL_RESULT\|phi(x,y)\|4*x^2 + 4*y^2 - x*y + 4*x + 2*y` | exact_ode_generator.py, line_integral_generator.py |
| `POW` | 2 | `POW\|(1/4)^1\|0.25` | binomial_probability_generator.py, geometric_distribution_generator.py, recurrence_generator.py |
| `POWER_ENTRY` | 3 | `POWER_ENTRY\|(1,1)\|27\|27` | diagonalization_generator.py |
| `POWER_FORM` | 1 | `POWER_FORM\|A^3 = P*D^3*P^-1` | diagonalization_generator.py |
| `POWER_INTEGRAL` | 2 | `POWER_INTEGRAL\|int_0^a x dx\|a^2/2` | continuous_distribution_generator.py, wavefunction_generator.py |
| `POWER_REDUCE` | 2 | `POWER_REDUCE\|55^124\|55^4 mod 84` | totient_generator.py |
| `POWER_RULE` | 2 | `POWER_RULE\|-7x^2\|-14x` | chain_rule_generator.py, commutator_generator.py, curve_analysis_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, mean_value_theorem_generator.py, optimization_generator.py, tangent_line_generator.py |
| `POWER_SETUP` | 2 | `POWER_SETUP\|(e^(i*124 deg))^(4i)\|principal logarithm` | complex_log_generator.py |
| `POWER_SET_RESULT` | 1 | `POWER_SET_RESULT\|{∅, {j}, {p}, {s}, {j, p}, {j, s}, {p, s}, {j, p, s}}` | set_operations_generator.py |
| `POWER_SHIFT` | 3 | `POWER_SHIFT\|k=0\|0-2\|-2` | laurent_series_generator.py |
| `PREDICATES` | 1 | `PREDICATES\|H(x): x is a baker; U(y): y is a teacher; P(x, y): x mentors y` | english_to_logic_generator.py |
| `PREDICT` | 2 | `PREDICT\|x*\|12/11` | kernel_ridge_generator.py |
| `PREIMAGE` | 2 | `PREIMAGE\|2\|{g}` | function_properties_generator.py |
| `PREMISE` | 2 | `PREMISE\|1\|c` | natural_deduction_generator.py |
| `PREMISES_ALL_T` | 2 | `PREMISES_ALL_T\|r=T, s=T\|no` | argument_form_generator.py |
| `PRIME` | 1 | `PRIME\|41` | divisibility_classification_generator.py |
| `PRIM_CANDIDATES` | 2 | `PRIM_CANDIDATES\|visited A\|AE=2, AB=3, AD=6, AC=12` | mst_generator.py |
| `PRIM_START` | 1 | `PRIM_START\|A` | mst_generator.py |
| `PRINCIPAL_LOG` | 1 | `PRINCIPAL_LOG\|ln(394) + i*13pi/20` | complex_log_generator.py |
| `PRINCIPAL_MINOR` | 2 | `PRINCIPAL_MINOR\|K11\|3` | kernel_validity_generator.py |
| `PRIOR_PRECISION` | 1 | `PRIOR_PRECISION\|1/tau^2` | bayesian_update_generator.py |
| `PROBABILITY` | 2 | `PROBABILITY\|P(+x)\|289/1250` | spin_half_generator.py |
| `PROB_CONDITIONAL` | 2 | `PROB_CONDITIONAL\|P(multiple of 4 given first was multiple of 4)\|3/16` | compound_probability_generator.py |
| `PROB_DEPENDENT` | 1 | `PROB_DEPENDENT\|Drawing without replacement means dependent events` | compound_probability_generator.py |
| `PROB_DESCRIBE` | 1 | `PROB_DESCRIBE\|Coin and d19: heads, then 11` | compound_probability_generator.py |
| `PROB_IDENTIFY` | 2 | `PROB_IDENTIFY\|P(heads)\|1/2` | compound_probability_generator.py |
| `PROB_INDEPENDENT` | 1 | `PROB_INDEPENDENT\|The coin flip and die roll are independent events` | compound_probability_generator.py |
| `PROB_MULTIPLY` | 3 | `PROB_MULTIPLY\|1/2\|1/19\|1/38` | compound_probability_generator.py |
| `PROB_SETUP` | 2 | `PROB_SETUP\|11\|16` | complement_probability_generator.py, counting_to_probability_generator.py, fundamental_counting_principle_generator.py, likelihood_language_generator.py, odds_probability_generator.py, random_digit_simulation_generator.py, sample_space_list_generator.py, simple_probability_generator.py, venn_probability_generator.py |
| `PROB_SIMPLIFY` | 2 | `PROB_SIMPLIFY\|12/272\|3/68` | compound_probability_generator.py |
| `PROB_WEIGHT` | 2 | `PROB_WEIGHT\|0^2\|0` | clebsch_gordan_generator.py |
| `PRODUCT` | 2 | `PRODUCT\|Delta x^2 * Delta p^2\|25600pi^2/12 - 1/2` | uncertainty_generator.py |
| `PROJECT` | 2 | `PROJECT\|P1\|8` | pca_generator.py |
| `PROJECTILE_SETUP` | 3 | `PROJECTILE_SETUP\|vx=55\|vy=29\|g=10` | projectile_motion_generator.py |
| `PROJECTION` | 2 | `PROJECTION\|X*beta\|[11, 7, 3, -1]` | least_squares_generator.py, legendre_construction_generator.py |
| `PROJECTOR_SETUP` | 2 | `PROJECTOR_SETUP\|v=(151800/151801, 551/151801)\|P=vv^T=[[23043240000/23043543601,83641800/23043543601],[83641800/23043543601,303601/23043543601]]` | projector_generator.py |
| `PROJ_COEFF` | 3 | `PROJ_COEFF\|v2 on u1\|-15/5\|-3` | gram_schmidt_generator.py |
| `PROJ_VECTOR` | 2 | `PROJ_VECTOR\|-3*u1\|[6, 3]` | gram_schmidt_generator.py |
| `PROPERTY_MATCH` | 3 | `PROPERTY_MATCH\|multiplicative identity property\|a × 1 = a\|5771 × 1` | operation_properties_generator.py |
| `PROPERTY_RESULT` | 2 | `PROPERTY_RESULT\|reflexive\|no` | relation_check_generator.py |
| `PROP_SETUP` | 1 | `PROP_SETUP\|2/2 = x/3` | proportion_word_problem_generator.py, proportional_relationship_generator.py, similar_triangles_generator.py, triangle_solve_generator.py |
| `PSD_SETUP` | 2 | `PSD_SETUP\|K=[[3,-10], [-10,12]]\|criterion=all principal minors >= 0` | kernel_validity_generator.py |
| `PULL` | 2 | `PULL\|∀x\|from left past ∧` | prenex_normal_form_generator.py |
| `PURITY` | 1 | `PURITY\|Tr(rho^2)=29/49` | density_matrix_generator.py |
| `PYTHAG_CALCULATE` | 2 | `PYTHAG_CALCULATE\|d² = 921600 + 414736 = 1336336\|1336336` | pythag_leg_generator.py |
| `PYTHAG_CONTEXT` | 3 | `PYTHAG_CONTEXT\|rectangle_diagonal\|length=960, width=644\|diagram=YCB` | pythag_leg_generator.py |
| `PYTHAG_FORMULA` | 1 | `PYTHAG_FORMULA\|a² + b² = c²` | pythag_hyp_generator.py, pythag_leg_generator.py |
| `PYTHAG_MODEL` | 3 | `PYTHAG_MODEL\|length=960\|width=644\|diagonal=?` | pythag_leg_generator.py |
| `PYTHAG_ROOT` | 2 | `PYTHAG_ROOT\|2601\|51` | pythag_leg_generator.py |
| `PYTHAG_SETUP` | 2, 3 | `PYTHAG_SETUP\|legs=1170,168\|hypotenuse QU=?` | pythag_hyp_generator.py, pythag_leg_generator.py |
| `PYTHAG_SOLVE` | 2 | `PYTHAG_SOLVE\|b² = 22201 - 19600\|2601` | pythag_leg_generator.py |
| `PYTHAG_SQUARE` | 2 | `PYTHAG_SQUARE\|140\|19600` | pythag_leg_generator.py |
| `PYTHAG_SUBSTITUTE` | 1 | `PYTHAG_SUBSTITUTE\|140² + b² = 149²` | pythag_leg_generator.py |
| `Q1` | 4 | `Q1\|80\|400\|40\|12` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `Q2` | 4 | `Q2\|80\|400\|40\|-8` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `QN_ADD` | 4 | `QN_ADD\|Q\|left\|0 + pi+(1)\|1` | conservation_law_generator.py |
| `QR_ENTRY` | 2 | `QR_ENTRY\|q1\|[1, 0, 0]` | qr_decomposition_generator.py |
| `QR_SETUP` | 2 | `QR_SETUP\|A = [[2, -2, 5], [0, 6, 2], [0, 0, 5]]\|Gram-Schmidt columns` | qr_decomposition_generator.py |
| `QUADRANT` | 2 | `QUADRANT\|135°\|quadrant II` | angle_measure_generator.py, polar_parametric_generator.py, unit_circle_generator.py |
| `QUADRATIC` | 3 | `QUADRATIC\|2\|-10\|8` | mobius_transform_generator.py |
| `QUANTUM_FORMULA` | 1 | `QUANTUM_FORMULA\|lambda=h/p` | quantum_formula_generator.py |
| `QUANTUM_SETUP` | 2, 3 | `QUANTUM_SETUP\|gate=H\|input=e^(i51π/91)·ket1` | quantum_formula_generator.py, quantum_gate_generator.py |
| `QUANT_CASE` | 1, 2 | `QUANT_CASE\|x=18` | quantifier_finite_domain_generator.py |
| `QUANT_CHOICE` | 1 | `QUANT_CHOICE\|some → ∃; some → ∃` | english_to_logic_generator.py |
| `QUANT_RESULT` | 2, 3 | `QUANT_RESULT\|∃x ∀y\|true` | quantifier_finite_domain_generator.py |
| `QUANT_SETUP` | 3 | `QUANT_SETUP\|x=(151/100,-49/25,99/100)\|scale=1/20\|zero_point=-6` | quantization_generator.py |
| `QUANT_VALUE` | 2 | `QUANT_VALUE\|1\|24` | quantization_generator.py |
| `QUARK_CHARGE` | 2 | `QUARK_CHARGE\|anti_u\|-2/3` | quark_composition_generator.py |
| `QUARK_SETUP` | 3 | `QUARK_SETUP\|antibaryon,count=700\|anti_u anti_s anti_b\|u=2/3,d=-1/3,s=-1/3,c=2/3,b=-1/3; anti=-charge` | quark_composition_generator.py |
| `QUARTILE` | 3 | `QUARTILE\|Q1\|10,12,14,15,16\|14` | five_number_summary_generator.py |
| `QUAT_COMPONENT` | 3 | `QUAT_COMPONENT\|p*q\|real\|-7` | quaternion_generator.py |
| `QUAT_INVERSE` | 2 | `QUAT_INVERSE\|p\|(-1/6,-1/18,1/9,1/9)` | quaternion_generator.py |
| `QUAT_MUL_START` | 3 | `QUAT_MUL_START\|p*q\|p\|q` | quaternion_generator.py |
| `QUAT_RESULT` | 2 | `QUAT_RESULT\|p*q\|(-7,11,-12,10)` | quaternion_generator.py |
| `QUAT_SETUP` | 2 | `QUAT_SETUP\|p=(-3,1,-2,-2)\|q=(2,1,3,-3)` | quaternion_generator.py |
| `QUEUE_STATE` | 2 | `QUEUE_STATE\|initial\|D` | graph_traversal_generator.py |
| `QUOTIENT` | 1 | `QUOTIENT\|x^3 + x^2 + 1` | finite_field_generator.py |
| `Q_EXPR` | 1 | `Q_EXPR\|Q = [B]/[A]` | equilibrium_ice_generator.py |
| `R` | 1 | `R\|21` | complex_number_ops_generator.py, finite_field_generator.py, long_division_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `RANGE` | 1 | `RANGE\|{18, 27, 30}` | relation_operations_generator.py |
| `RANK` | 2 | `RANK\|∅\|0` | hereditarily_finite_set_generator.py |
| `RAPIDITY_SUM` | 2 | `RAPIDITY_SUM\|collinear boosts\|-1/6` | minkowski_interval_generator.py |
| `RATE_MONTHLY` | 2 | `RATE_MONTHLY\|24% / 12\|0.02` | finance_generator.py |
| `RATE_SETUP` | 2 | `RATE_SETUP\|30 m ladder; the base slides away at 10 m/min; base is 18 m from the wall\|dy/dt` | related_rates_generator.py |
| `RATIO` | 2, 3 | `RATIO\|y = 2*x\|y = 2*x` | lagrange_multiplier_generator.py, simplex_generator.py |
| `RATIONALIZE` | 1 | `RATIONALIZE\|√233/√233` | dot_product_generator.py, limit_evaluation_generator.py, radical_rationalize_generator.py, special_right_triangle_generator.py |
| `RATIO_BASE` | 3 | `RATIO_BASE\|14:12\|2\|7:6` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RATIO_TABLE` | 2 | `RATIO_TABLE\|Trees: 14, 42, 77, ?\|Rows: 12, 36, 66, 72` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RAW_FORMULA` | 1 | `RAW_FORMULA\|x = μ + z·σ` | z_score_generator.py |
| `REARRANGE_EQ` | 1 | `REARRANGE_EQ\|whole = 36335 / 0.845` | percent_problem_generator.py |
| `RECIPROCAL` | 2 | `RECIPROCAL\|csc θ = 1/sin θ\|-41/9` | trig_six_functions_generator.py |
| `RECOVER_DATA` | 2 | `RECOVER_DATA\|positions 3,5,6,7\|1010` | hamming_code_generator.py |
| `RECT_FORM` | 1 | `RECT_FORM\|30` | de_moivre_generator.py, euler_formula_generator.py |
| `RECUR` | 3 | `RECUR\|4P_4 = 7x P_3 - 3P_2\|P_3 = (5x^3 - 3x)/2\|P_2 = (3x^2 - 1)/2` | legendre_construction_generator.py |
| `RECURRENCE` | 2 | `RECURRENCE\|a_(n+1)\|2a_n/(n+1)` | derangement_generator.py, series_solution_generator.py |
| `REC_SETUP` | 1, 2 | `REC_SETUP\|a_n = -5 a_(n-1) - 6 a_(n-2) - 12\|a_0 = -1, a_1 = -3` | master_theorem_generator.py, recurrence_generator.py |
| `REDUCE` | 2, 3 | `REDUCE\|(74, 50)\|(24, 0)` | integers_as_pairs_generator.py, rationals_as_pairs_generator.py |
| `REDUCED_DENSITY` | 1 | `REDUCED_DENSITY\|rho_A=[[1/2,0],[0,1/2]]` | partial_trace_generator.py |
| `REFLEXIVE_CHECK` | 2 | `REFLEXIVE_CHECK\|(2, 2)\|present` | equivalence_relation_generator.py, relation_check_generator.py |
| `REGEX_ACCEPT` | 1 | `REGEX_ACCEPT\|q80877_3, q80877_4` | regex_to_automaton_generator.py |
| `REGEX_SETUP` | 3 | `REGEX_SETUP\|(a or b)*(ab or ba)\|alphabet a,b\|canonical progress DFA` | regex_to_automaton_generator.py |
| `REGEX_STATE` | 2 | `REGEX_STATE\|q80877_0\|start` | regex_to_automaton_generator.py |
| `REGEX_TRANSITION` | 3 | `REGEX_TRANSITION\|q80877_0\|a\|q80877_1` | regex_to_automaton_generator.py |
| `REGION` | 2 | `REGION\|both\|{17, 19, 25}` | attribute_sorting_generator.py, venn_region_count_generator.py |
| `REGION_EQ` | 2 | `REGION_EQ\|A ∩ B\|11` | venn_region_count_generator.py |
| `REGION_MEASURE` | 3 | `REGION_MEASURE\|area\|5*3\|15` | vector_theorem_generator.py |
| `REGION_REWRITE` | 2 | `REGION_REWRITE\|0 <= y <= 10\|y/2 <= x <= 5` | double_integral_generator.py |
| `REG_ROW` | 3 | `REG_ROW\|x-x̄=-2\|y-ȳ=2\|product=-4` | regression_generator.py |
| `REG_SETUP` | 2 | `REG_SETUP\|points: (1, 40), (2, 38), (3, 34), (4, 42), (5, 36)\|least-squares line` | regression_generator.py |
| `REJECT` | 1, 2 | `REJECT\|x = −21` | cantor_pairing_generator.py, conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, knights_knaves_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py, structure_isomorphism_generator.py |
| `RELAX` | 3 | `RELAX\|E->A\|update inf to 9\|via weight 9` | dijkstra_generator.py |
| `RELU` | 3 | `RELU\|z=-3\|h=0\|deriv=0` | backprop_generator.py |
| `REL_ENERGY_FORMULA` | 1 | `REL_ENERGY_FORMULA\|E=sqrt(p^2+m^2)` | relativistic_energy_generator.py |
| `REL_ENERGY_SETUP` | 3 | `REL_ENERGY_SETUP\|energy_momentum\|c=1\|p=252, m=405` | relativistic_energy_generator.py |
| `REL_FORMULA` | 1 | `REL_FORMULA\|t=gamma*tau` | special_relativity_generator.py |
| `REL_FREQ` | 3 | `REL_FREQ\|amber\|33/57\|11/19` | experimental_probability_generator.py |
| `REL_PAIR` | 2 | `REL_PAIR\|(12, 12)\|same block` | equivalence_relation_generator.py |
| `REL_SETUP` | 2, 3 | `REL_SETUP\|A = {2, 17, 18, 26, 52, 59}\|R = {(2, 2), (2, 17), (2, 52), (2, 59), (17, 2), (17, 17), (17, 52), (17, 59), (18, 18), (18, 26), (26, 18), (26, 26), (52, 2), (52, 17), (52, 52), (52, 59), (59, 2), (59, 17), (59, 52), (59, 59)}` | equivalence_relation_generator.py, relation_check_generator.py, relation_closure_generator.py, relation_operations_generator.py, special_relativity_generator.py |
| `RENAME` | 2 | `RENAME\|∃x\|∃x1` | prenex_normal_form_generator.py |
| `RENORMALIZE` | 3 | `RENORMALIZE\|d\|(14/153)/(71/153)\|14/71` | probability_measure_generator.py |
| `REPEAT_DETECT` | 2 | `REPEAT_DETECT\|remainder 52 repeats\|repetend 228070175438596491` | repeating_decimal_generator.py |
| `REPRESENT` | 2 | `REPRESENT\|e ∣ p\|p = ex` | direct_proof_algebra_generator.py |
| `REP_DIM` | 2 | `REP_DIM\|8\|8` | young_tableaux_generator.py |
| `RESIDUAL` | 2 | `RESIDUAL\|y - X*beta\|[-3, 3, 3, -3]` | least_squares_generator.py |
| `RESIDUE` | 1, 3 | `RESIDUE\|7` | contour_integral_generator.py, residue_generator.py |
| `RESIDUE_SETUP` | 2 | `RESIDUE_SETUP\|a=-3\|f=7/(z+3) - 1 - 3(z+3)` | residue_generator.py |
| `RESIDUE_SUM` | 1 | `RESIDUE_SUM\|10` | contour_integral_generator.py |
| `RESID_SETUP` | 2 | `RESID_SETUP\|point (1, 42), line ŷ = 45.8 - 0.6x\|residual = observed − predicted` | regression_generator.py |
| `RESOLVE` | 3 | `RESOLVE\|C1\|C2\|¬P320` | resolution_proof_generator.py |
| `RESTRICT_CHECK` | 3 | `RESTRICT_CHECK\|(a, 17)\|a in D=yes\|keep` | relation_operations_generator.py |
| `RES_EMPTY` | 1 | `RES_EMPTY\|C7` | resolution_proof_generator.py |
| `RES_SETUP` | 1 | `RES_SETUP\|C1=(¬P320), C2=(P14166 ∨ P320), C3=(¬P14166), C4=(¬P70457 ∨ ¬P90594)` | resolution_proof_generator.py |
| `RES_SKIP` | 3 | `RES_SKIP\|C1\|C2\|(P14166)` | resolution_proof_generator.py |
| `REVERSE` | 2 | `REVERSE\|0,0,0,1,1,1,1,1\|11111000` | base_arithmetic_generator.py, base_conversion_generator.py, bitwise_ops_generator.py |
| `REWRITE` | 1, 2 | `REWRITE\|5771 × 1\|5771` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, cardinal_arithmetic_generator.py, chain_rule_generator.py, circle_equation_generator.py, combinatory_logic_generator.py, completing_square_generator.py, complex_division_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, domain_range_generator.py, dot_product_generator.py, english_to_logic_generator.py, euler_formula_generator.py, evaluate_expression_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, frequency_table_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, implicit_diff_generator.py, improper_integral_generator.py, induction_verify_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, inverse_function_generator.py, lambda_reduction_generator.py, laurent_series_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logical_equivalence_laws_generator.py, logistic_growth_generator.py, master_theorem_generator.py, matrix_inverse_generator.py, method_of_moments_generator.py, mgf_generator.py, midpoint_generator.py, mle_generator.py, normal_table_generator.py, ode_substitution_generator.py, operation_properties_generator.py, optimization_generator.py, order_of_operations_generator.py, ordinal_arithmetic_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, permutation_combination_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, power_series_generator.py, prenex_normal_form_generator.py, quadratic_factoring_generator.py, quantifier_negation_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, right_triangle_trig_generator.py, row_reduction_generator.py, separable_ode_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_algebra_laws_generator.py, set_expression_generator.py, set_operations_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, spin_half_generator.py, standard_form_conversion_generator.py, stars_and_bars_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, u_substitution_generator.py, vector_ops_generator.py, z_transform_generator.py |
| `RG_SETUP` | 3 | `RG_SETUP\|one_loop\|alpha0=2/19\|beta=4,L=1/3` | running_coupling_generator.py |
| `RHO_ITER` | 4 | `RHO_ITER\|1\|x=67, y=33\|abs(r)=34\|gcd=1` | pollard_factorization_generator.py |
| `RICCI_ENTRY` | 2 | `RICCI_ENTRY\|R_phiphi\|1` | riemann_tensor_generator.py |
| `RIDGE_ENTRY` | 2 | `RIDGE_ENTRY\|K\|[[25,20], [20,16]]` | kernel_ridge_generator.py |
| `RIEMANN_ENTRY` | 2 | `RIEMANN_ENTRY\|R^phi_theta phi theta\|20736/21025` | riemann_tensor_generator.py |
| `RIEMANN_SETUP` | 2, 3 | `RIEMANN_SETUP\|f(x) = x^2 on [-2, 6], n = 4\|right Riemann sum` | riemann_sum_generator.py, riemann_tensor_generator.py |
| `RK_COMBINE` | 2 | `RK_COMBINE\|k1+2k2+2k3+k4\|-153/5` | runge_kutta_generator.py |
| `RK_STAGE` | 3 | `RK_STAGE\|k1\|x=1\|w=1/2` | runge_kutta_generator.py |
| `RODRIGUES_FORM` | 2 | `RODRIGUES_FORM\|e^(theta K)\|I + sin(theta)K + (1-cos(theta))K^2` | lie_exponential_generator.py |
| `ROOT` | 1, 2, 3 | `ROOT\|625\|25` | ac_circuit_generator.py, adam_step_generator.py, cholesky_generator.py, completing_square_generator.py, confidence_interval_generator.py, countability_bijection_generator.py, de_moivre_generator.py, doppler_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, factor_special_forms_generator.py, four_vector_generator.py, fundamental_form_generator.py, hypothesis_test_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, ladder_operator_generator.py, layer_norm_generator.py, low_rank_approx_generator.py, matrix_norm_generator.py, metric_arc_length_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, planck_units_generator.py, pythag_hyp_generator.py, qr_decomposition_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, regression_generator.py, relativistic_energy_generator.py, round_solids_generator.py, rv_transform_generator.py, schwarzschild_generator.py, shm_generator.py, svd_generator.py, svm_margin_generator.py, two_sample_test_generator.py |
| `ROOT_ANGLE` | 2 | `ROOT_ANGLE\|k=0\|0 deg` | de_moivre_generator.py |
| `ROOT_EXTRACT` | 2 | `ROOT_EXTRACT\|3` | exponent_generator.py |
| `ROOT_IDENTIFY` | 3 | `ROOT_IDENTIFY\|27\|perfect_cube\|3` | exponent_generator.py |
| `ROOT_SETUP` | 1 | `ROOT_SETUP\|∛27` | exponent_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `ROOT_SIMPLIFY` | 1, 2 | `ROOT_SIMPLIFY\|6√10` | complex_quadratic_generator.py, distance_formula_generator.py, dot_product_generator.py, euler_formula_generator.py, exponent_generator.py, geometric_mean_generator.py, hypercube_counting_generator.py, polar_parametric_generator.py, vector_ops_generator.py |
| `ROSTER` | 2 | `ROSTER\|S\|{−22, −20, −18, −16, −14, −12, −10, −8}` | set_builder_roster_generator.py |
| `ROTATED_VECTOR` | 1 | `ROTATED_VECTOR\|(3,-4,-3)` | quaternion_generator.py |
| `ROT_FORMULA` | 1 | `ROT_FORMULA\|I=I_cm+m*d^2` | rotational_dynamics_generator.py |
| `ROT_SETUP` | 3 | `ROT_SETUP\|parallel_axis\|I_cm=19, m=16\|d=1` | rotational_dynamics_generator.py |
| `ROUND` | 2 | `ROUND\|121/5\|24` | quantization_generator.py |
| `ROUNDTRIP_ERROR` | 2 | `ROUNDTRIP_ERROR\|sum_abs\|3/100` | quantization_generator.py |
| `ROUND_CHECK` | 3 | `ROUND_CHECK\|4\|8\|>=5` | place_value_rounding_generator.py |
| `ROUND_RESULT` | 2 | `ROUND_RESULT\|19148\|19150` | place_value_rounding_generator.py |
| `ROUTH_ROW` | 2 | `ROUTH_ROW\|s^3\|1, 30` | routh_hurwitz_generator.py |
| `ROUTH_SETUP` | 1 | `ROUTH_SETUP\|p(s)=s^3+8s^2+30s+46` | routh_hurwitz_generator.py |
| `ROW` | 2 | `ROW\|b=F, j=T, n=F\|T` | foundations_critic_generator.py |
| `ROW_ENTROPY` | 2 | `ROW_ENTROPY\|H0\|649/800` | entropy_rate_markov_generator.py |
| `ROW_OP` | 1, 2 | `ROW_OP\|R2 → R2 - 3·R1\|[0, 1, 1]` | row_reduction_generator.py, simplex_generator.py, subspace_basis_generator.py |
| `RREF_RESULT` | 2 | `RREF_RESULT\|RREF(A)\|[[1, 0, -2, 1], [0, 1, 1, -1], [0, 0, 0, 0]]` | subspace_basis_generator.py |
| `RSA_DECRYPT` | 2 | `RSA_DECRYPT\|566\|126` | rsa_generator.py |
| `RSA_ENCRYPT` | 2 | `RSA_ENCRYPT\|126\|566` | rsa_generator.py |
| `RSA_PRIVATE_KEY` | 1 | `RSA_PRIVATE_KEY\|d=145` | rsa_generator.py |
| `RSA_PUBLIC_KEY` | 2 | `RSA_PUBLIC_KEY\|n=667\|e=17` | rsa_generator.py |
| `RSA_SETUP` | 3 | `RSA_SETUP\|p=23\|q=29\|message=126` | rsa_generator.py |
| `RSQ_FORMULA` | 1 | `RSQ_FORMULA\|r^2 = Sxy^2/(Sxx·Syy)` | regression_generator.py |
| `RS_CORRECT` | 2 | `RS_CORRECT\|position=3\|[114,75,17,70]` | reed_solomon_generator.py |
| `RS_EVAL` | 2 | `RS_EVAL\|x=5\|12` | reed_solomon_generator.py |
| `RS_LINE` | 3 | `RS_LINE\|m0=77\|m1=36\|agree=3` | reed_solomon_generator.py |
| `RS_PAIR` | 2 | `RS_PAIR\|x=60,75\|y=114,75` | reed_solomon_generator.py |
| `RS_RECEIVED` | 1 | `RS_RECEIVED\|[114,75,112,70]` | reed_solomon_generator.py |
| `RS_SETUP` | 3 | `RS_SETUP\|F_193\|RS(4,2)\|points 60,75,127,166; one error allowed` | reed_solomon_generator.py |
| `RUNNING_TOTAL` | 3 | `RUNNING_TOTAL\|0\|4096\|4096` | function_properties_generator.py |
| `S` | 3 | `S\|632\|594\|38` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arc_length_generator.py, area_between_curves_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, backprop_generator.py, bayesian_update_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, black_scholes_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, cantor_pairing_generator.py, casimir_force_generator.py, casimir_generator.py, channel_capacity_generator.py, cholesky_generator.py, circle_angle_generator.py, circle_equation_generator.py, collision_generator.py, commutator_generator.py, complement_probability_generator.py, complex_locus_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, countability_bijection_generator.py, counting_classics_generator.py, cramers_rule_generator.py, decimal_div_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, determinant_generator.py, dft_generator.py, distance_formula_generator.py, doppler_generator.py, ellipse_features_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, entropy_generator.py, equilibrium_ice_generator.py, euler_characteristic_generator.py, euler_circuit_generator.py, euler_method_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, finance_generator.py, finite_difference_generator.py, first_law_generator.py, five_number_summary_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, function_inner_product_generator.py, function_operations_generator.py, fundamental_counting_principle_generator.py, fundamental_form_generator.py, game_theory_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_sequence_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_interpret_generator.py, graph_traversal_generator.py, hamiltonian_generator.py, heat_engine_generator.py, hermitian_check_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, information_gain_generator.py, integrating_factor_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, layer_norm_generator.py, legendre_construction_generator.py, linear_simple_generator.py, logistic_growth_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mle_generator.py, mobius_transform_generator.py, modular_inverse_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, normal_table_generator.py, npv_irr_generator.py, ode_substitution_generator.py, ode_system_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, pca_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, permutation_group_generator.py, ph_calculation_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, pollard_factorization_generator.py, positive_definite_generator.py, probability_addition_rule_generator.py, probability_axioms_finite_generator.py, probability_measure_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recurrence_generator.py, regression_generator.py, related_rates_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, rv_transform_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_pde_generator.py, series_convergence_generator.py, set_counting_generator.py, shm_generator.py, signal_arithmetic_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solid_revolution_generator.py, special_relativity_generator.py, spherical_excess_generator.py, spin_half_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, totient_generator.py, transformation_generator.py, transportation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, two_sample_test_generator.py, two_way_table_probability_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, vector_ops_generator.py, venn_probability_generator.py, venn_region_count_generator.py, z_score_generator.py |
| `SAMPLE_MOMENT` | 2 | `SAMPLE_MOMENT\|xbar\|9` | method_of_moments_generator.py |
| `SAMPLE_SIZE_FORMULA` | 1 | `SAMPLE_SIZE_FORMULA\|n = (z*·σ/E)^2` | confidence_interval_generator.py |
| `SAMPLE_SPACE` | 3 | `SAMPLE_SPACE\|ordered digit cards\|17, 18, 71, 78, 81, 87\|6` | sample_space_list_generator.py |
| `SA_BASES` | 2 | `SA_BASES\|2π(21)² = 2π × 441\|882π` | volume_3d_generator.py |
| `SA_FACES` | 3 | `SA_FACES\|top/bottom\|9 × 3\|27` | volume_3d_generator.py |
| `SA_FORMULA` | 1 | `SA_FORMULA\|SA = 2(lw + lh + wh)` | round_solids_generator.py, volume_3d_generator.py |
| `SA_LATERAL` | 2 | `SA_LATERAL\|2π × 21 × 10\|420π` | volume_3d_generator.py |
| `SA_SETUP` | 2 | `SA_SETUP\|rectangular_prism\|l=9, w=3, h=6` | volume_3d_generator.py |
| `SA_TOTAL` | 2 | `SA_TOTAL\|SA = 2(27 + 54 + 18)\|198` | round_solids_generator.py, volume_3d_generator.py |
| `SB_FORMULA` | 1 | `SB_FORMULA\|C(n+k-1, k-1)` | stars_and_bars_generator.py |
| `SB_SETUP` | 2 | `SB_SETUP\|x1+...+x8 = 30\|xi >= 0` | stars_and_bars_generator.py |
| `SCALE_DIV` | 3 | `SCALE_DIV\|2726\|58\|47` | scaling_generator.py |
| `SCALE_EXACT` | 2 | `SCALE_EXACT\|30*cos\|30` | de_moivre_generator.py, euler_formula_generator.py |
| `SCALE_IDENTIFY` | 2 | `SCALE_IDENTIFY\|12.75 centimeters\|actual_dimension` | scaling_generator.py |
| `SCALE_MODE` | 3 | `SCALE_MODE\|λ = 2\|16*17\|272` | diagonalization_generator.py |
| `SCALE_MULT` | 3 | `SCALE_MULT\|12.75\|20\|255` | scaling_generator.py |
| `SCALE_SETUP` | 3 | `SCALE_SETUP\|1 centimeter\|20 meters\|20` | scaling_generator.py |
| `SCALE_SHIFT` | 2 | `SCALE_SHIFT\|1\|4` | layer_norm_generator.py |
| `SCALING_COMPUTE` | 2 | `SCALING_COMPUTE\|6ND\|12600000000000000000` | scaling_law_generator.py |
| `SCALING_SETUP` | 3 | `SCALING_SETUP\|N=60000000\|D=35000000000\|F=61000000000000000` | scaling_law_generator.py |
| `SCAN` | 2 | `SCAN\|q\|parenthesis depth 0` | wff_parsing_generator.py |
| `SCHWARZSCHILD_SETUP` | 3, 4 | `SCHWARZSCHILD_SETUP\|time_dilation\|r_s=160\|r=250` | schwarzschild_generator.py |
| `SCI_IDENTIFY` | 2 | `SCI_IDENTIFY\|3.29\|-1` | exponent_generator.py |
| `SCI_MOVE_DECIMAL` | 2 | `SCI_MOVE_DECIMAL\|right\|1` | exponent_generator.py |
| `SCI_OPERATION` | 4 | `SCI_OPERATION\|multiply_coefficients\|4.8\|2.1\|10.08` | exponent_generator.py |
| `SCI_SETUP` | 1 | `SCI_SETUP\|0.329` | exponent_generator.py |
| `SCORE_EQ` | 1 | `SCORE_EQ\|-7-8*mu=0` | mle_generator.py |
| `SEARCH_BOUNDS` | 3 | `SEARCH_BOUNDS\|iter 1\|lo=0\|hi=5` | algorithm_trace_generator.py |
| `SEARCH_STATE` | 2 | `SEARCH_STATE\|lo=3\|hi=5` | algorithm_trace_generator.py |
| `SECOND_DERIV_TEST` | 2 | `SECOND_DERIV_TEST\|f'' < 0 for x < 4, f'' > 0 for x > 4\|concavity changes` | curve_analysis_generator.py, optimization_generator.py |
| `SECOND_PARTIAL` | 2 | `SECOND_PARTIAL\|f_xx\|-4` | hessian_classify_generator.py |
| `SECTION_FORMULA` | 1 | `SECTION_FORMULA\|P = (x1 + m/(m+n)·(x2 - x1), y1 + m/(m+n)·(y2 - y1))` | segment_partition_generator.py |
| `SECTION_SETUP` | 2 | `SECTION_SETUP\|A(2, 4), B(-26, -10); ratio 4:3 from A\|point P` | segment_partition_generator.py |
| `SECTOR_FORMULA` | 1 | `SECTOR_FORMULA\|A = (1/2)r^2θ` | arc_sector_generator.py |
| `SELECT_MIN` | 2 | `SELECT_MIN\|E\|0` | dijkstra_generator.py |
| `SELECT_RELEVANT` | 2 | `SELECT_RELEVANT\|base = 47, rate = 15%\|ignore 44 (irrelevant)` | percent_word_problem_generator.py, proportion_word_problem_generator.py |
| `SEPARATE` | 1, 2 | `SEPARATE\|dy/y = -7 dt` | ode_substitution_generator.py, separable_ode_generator.py, separable_pde_generator.py |
| `SEPARATOR` | 3 | `SEPARATOR\|16/11\|in L(3/2)\|not in L(√2)` | dedekind_cut_generator.py |
| `SEQ_APPLY` | 1 | `SEQ_APPLY\|a_12 = 4 + (12 - 1)·-9` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_FORMULA` | 1 | `SEQ_FORMULA\|a_n = a_1 + (n - 1)d` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_SETUP` | 2 | `SEQ_SETUP\|4, -5, -14, -23, ...\|sum of first 12 terms` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SERIES` | 1 | `SERIES\|G=G1*G2` | transfer_function_generator.py |
| `SERIES_ASSUME` | 2 | `SERIES_ASSUME\|y\|sum a_n x^n` | series_solution_generator.py |
| `SERIES_GROUP` | 2 | `SERIES_GROUP\|even powers\|cos(theta)I` | lie_exponential_generator.py |
| `SERIES_SETUP` | 2 | `SERIES_SETUP\|Σ 1/(n^2 + 68), n ≥ 1\|converge or diverge?` | legendre_construction_generator.py, power_series_generator.py, series_convergence_generator.py |
| `SERIES_TERM` | 3 | `SERIES_TERM\|n=0\|1\|1` | grassmann_generator.py |
| `SETUP` | 1, 2 | `SETUP\|assume n is odd; show n + 1 is even` | direct_proof_algebra_generator.py, induction_verify_generator.py |
| `SETUP_PERCENT_EQ` | 1 | `SETUP_PERCENT_EQ\|percent_dec = 81198 / 46800` | percent_problem_generator.py |
| `SET_SETUP` | 2, 3, 4 | `SET_SETUP\|A = {o}\|B = {a, h, j, k, p, r}\|A Δ B` | set_expression_generator.py, set_operations_generator.py |
| `SET_SIDE` | 2 | `SET_SIDE\|left\|∅` | counterexample_search_generator.py |
| `SHAPE` | 1 | `SHAPE\|subject/object noun phrases restrict their quantifiers` | english_to_logic_generator.py |
| `SHIFT` | 1, 2 | `SHIFT\|yi = xi - 1\|y1+...+y6 = 49` | algorithm_trace_generator.py, recurrence_generator.py, stars_and_bars_generator.py, z_transform_generator.py |
| `SHM_FORMULA` | 1 | `SHM_FORMULA\|omega^2=k/m` | shm_generator.py |
| `SHM_SETUP` | 3 | `SHM_SETUP\|mass_spring_energy\|m=14, k=126\|A=3, x=2` | shm_generator.py |
| `SHORTEST` | 2 | `SHORTEST\|(2,-1)\|norm^2=5` | lll_reduction_generator.py |
| `SIDE` | 2 | `SIDE\|left\|∉` | set_identity_membership_table_generator.py |
| `SIGFIG_ROUND` | 3 | `SIGFIG_ROUND\|72000\|2 significant figures\|7.2 × 10^4` | fermi_estimation_generator.py |
| `SIGMA_EXPAND` | 1 | `SIGMA_EXPAND\|(-25) + (-15) + (-5) + 5 + 15 + 25 + 35` | sigma_notation_generator.py |
| `SIGMA_SETUP` | 2 | `SIGMA_SETUP\|Σ_(k=-3)^(3) (10k + 5)\|expand and evaluate` | sigma_notation_generator.py |
| `SIGMA_TERM` | 3 | `SIGMA_TERM\|k=-3\|10(-3) + 5\|-25` | sigma_notation_generator.py |
| `SIGN` | 3 | `SIGN\|left\|-8\|negative` | bisection_generator.py |
| `SIGNAL_SETUP` | 2, 3 | `SIGNAL_SETUP\|dB power ratio\|P2/P1=1/10` | signal_arithmetic_generator.py |
| `SIGN_CHART` | 2 | `SIGN_CHART\|zeros\|-1, 7` | polynomial_inequality_generator.py |
| `SIGN_RULE` | 2 | `SIGN_RULE\|arcsin of a negative\|negative angle` | trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `SIGN_TEST` | 4 | `SIGN_TEST\|(-inf, -11)\|y = -12\|f(y) = 12 (positive)\|up` | stability_generator.py |
| `SIMILAR_APPLY` | 3 | `SIMILAR_APPLY\|10\|2.5\|25` | scaling_generator.py |
| `SIMILAR_SCALE` | 3 | `SIMILAR_SCALE\|12\|4\|3` | scaling_generator.py |
| `SIMILAR_SETUP` | 3 | `SIMILAR_SETUP\|square\|4\|12` | scaling_generator.py |
| `SIMPLEX_SETUP` | 3 | `SIMPLEX_SETUP\|max z=6x+4y\|x<=6\|y<=6` | simplex_generator.py |
| `SIM_SETUP` | 2 | `SIM_SETUP\|△ABC ~ △DEF; AB = 16, DE = 32, BC = 12\|find EF` | similar_triangles_generator.py |
| `SIN` | 2 | `SIN\|3pi/2\|-1` | positional_encoding_generator.py |
| `SINGULAR_VALUE` | 2 | `SINGULAR_VALUE\|sigma1\|7` | low_rank_approx_generator.py |
| `SINUSOID_SETUP` | 2 | `SINUSOID_SETUP\|y = -2sin(6x - 270°) - 5\|amplitude, period, phase shift, midline` | sinusoid_features_generator.py |
| `SIZE_REDUCE` | 2 | `SIZE_REDUCE\|b2=(4, -9)\|b2-(-2)b1=(-2, 1)` | lll_reduction_generator.py |
| `SLOPE_CALC` | 2 | *(not observed in sampling)* | equation_from_two_points_generator.py |
| `SLOPE_FORMULA` | 1 | `SLOPE_FORMULA\|m = (y2 - y1) / (x2 - x1)` | equation_from_two_points_generator.py, regression_generator.py, slope_two_points_generator.py |
| `SLOPE_INT_IDENTIFY` | 2 | `SLOPE_INT_IDENTIFY\|Slope (m)\|-26` | slope_intercept_form_generator.py |
| `SLOPE_INT_MATCH` | 2 | `SLOPE_INT_MATCH\|Compare to Slope-Intercept Form\|y = mx + b` | slope_intercept_form_generator.py |
| `SLOPE_INT_SETUP` | 1 | `SLOPE_INT_SETUP\|y = -8 - 26x` | slope_intercept_form_generator.py |
| `SLOPE_RESULT` | 1 | `SLOPE_RESULT\|0` | equation_from_two_points_generator.py |
| `SLOPE_SETUP` | 2 | `SLOPE_SETUP\|(9, -3)\|(8, 8)` | slope_two_points_generator.py |
| `SLOPE_SUBST` | 1 | `SLOPE_SUBST\|m = (8 - (-3)) / (8 - 9)` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_UNDEFINED` | 1 | `SLOPE_UNDEFINED\|Division by zero` | slope_two_points_generator.py |
| `SOFTMAX_EXP` | 2 | `SOFTMAX_EXP\|1,1\|1` | attention_generator.py, softmax_gradient_generator.py |
| `SOFTMAX_PROB` | 2 | `SOFTMAX_PROB\|1\|1/6` | softmax_gradient_generator.py |
| `SOFTMAX_SETUP` | 3 | `SOFTMAX_SETUP\|z=(1*ln(2),1*ln(6),1*ln(4))\|T=1\|target=3` | softmax_gradient_generator.py |
| `SOFTMAX_WEIGHT` | 2 | `SOFTMAX_WEIGHT\|1,1\|1/3` | attention_generator.py |
| `SOLUTIONS` | 2 | `SOLUTIONS\|tan x = 0\|0°, 180°, 360°, 540°, 720°, 900°, 1080°, 1260°, 1440°, 1620°, 1800°, 1980°, 2160°, 2340°, 2520°, 2700°, 2880°, 3060°, 3240°, 3420°, 3600°, 3780°, 3960°, 4140°, 4320°, 4500°, 4680°, 4860°, 5040°, 5220°, 5400°, 5580°, 5760°, 5940°, 6120°, 6300°, 6480°, 6660°, 6840°, 7020°, 7200°, 7380°, 7560°, 7740°, 7920°, 8100°, 8280°, 8460°, 8640°, 8820°, 9000°, 9180°, 9360°, 9540°, 9720°, 9900°` | trig_equation_generator.py |
| `SOLUTION_FORMULA` | 1 | `SOLUTION_FORMULA\|M1*V1=M2*V2` | solution_chem_generator.py |
| `SOLUTION_SETUP` | 3 | `SOLUTION_SETUP\|dilution_stock_volume\|M1=2\|M2=1/4, V2=197` | solution_chem_generator.py |
| `SOLVE_CONST` | 2 | `SOLVE_CONST\|C1 = -1\|C2 = 2` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py |
| `SOLVE_U` | 2 | `SOLVE_U\|e^(-x)u = 3e^(-x) + C\|u = 3 + Ce^x` | ode_substitution_generator.py |
| `SOLVE_Y` | 2 | `SOLVE_Y\|e^(5x)y = 5e^(5x) + C\|y = 5 + Ce^(-5x)` | integrating_factor_generator.py, laplace_ivp_generator.py, ode_substitution_generator.py |
| `SOL_ENTRY` | 3 | `SOL_ENTRY\|x1(t)\|(-35*e^(5t) + 36*e^(6t))*(-3) + (-42*e^(5t) + 42*e^(6t))*5\|-105*e^(5t) + 102*e^(6t)` | matrix_exponential_generator.py |
| `SOL_FORM` | 1, 2 | `SOL_FORM\|y = (C1 + C2x)e^(3x)` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `SORT` | 2 | `SORT\|9,15,20,2,1\|1,2,9,15,20` | five_number_summary_generator.py, simple_stats_generator.py |
| `SORT_EDGES` | 1 | `SORT_EDGES\|AB=3, BE=5, AD=11, CE=12, AC=14, EF=15, CF=16` | mst_generator.py |
| `SPECIAL_SOLUTION` | 2 | `SPECIAL_SOLUTION\|18 = 21\|contradiction: no value of x works` | radical_equation_generator.py, special_solution_equation_generator.py |
| `SPEED` | 2, 3 | `SPEED\|sqrt(a^2 + b^2)\|sqrt(5^2 + 12^2)\|13` | curve_geometry_generator.py |
| `SPHERICAL_BOUNDS` | 2 | `SPHERICAL_BOUNDS\|rho\|0..8` | triple_integral_generator.py |
| `SPHERICAL_CONVERT` | 2 | `SPHERICAL_CONVERT\|6 dV\|6*rho^2*sin(phi) drho dphi dtheta` | triple_integral_generator.py |
| `SPHERICAL_COSINES` | 1 | `SPHERICAL_COSINES\|cos(c)=sin(lat1)sin(lat2)+cos(lat1)cos(lat2)cos(dlon)` | great_circle_generator.py |
| `SPHERICAL_COSINE_LAW` | 1 | `SPHERICAL_COSINE_LAW\|cos(a)=cos(b)cos(c)+sin(b)sin(c)cos(A)` | spherical_triangle_generator.py |
| `SPHERICAL_EXCESS_SETUP` | 2 | `SPHERICAL_EXCESS_SETUP\|R=15\|angles=150,75,30` | spherical_excess_generator.py |
| `SPHERICAL_SINE_LAW` | 1 | `SPHERICAL_SINE_LAW\|sin(A)/sin(a)=sin(B)/sin(b)` | spherical_triangle_generator.py |
| `SPHERICAL_TRIANGLE_SETUP` | 2 | `SPHERICAL_TRIANGLE_SETUP\|a=120 deg, b=120 deg, A=120 deg\|find sin(B)` | spherical_triangle_generator.py |
| `SPIN_COMPONENT` | 2 | `SPIN_COMPONENT\|row=1\|3/5` | spin_half_generator.py |
| `SPIN_SETUP` | 3 | `SPIN_SETUP\|measurement_probability\|axis=x\|psi=[-7/25,24/25]` | spin_half_generator.py |
| `SPLIT_MIDDLE` | 2 | `SPLIT_MIDDLE\|19y = 4y + 15y\|6y^2 + 4y + 15y + 10` | factor_trinomial_generator.py |
| `SPLIT_SETUP` | 3 | `SPLIT_SETUP\|source\|left pos=2, neg=6\|right pos=2, neg=6` | information_gain_generator.py |
| `SQRT_BOTH_SIDES` | 2 | `SQRT_BOTH_SIDES\|(x + 79)^2 = 2809\|x + 79 = ±53` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `SQRT_DIGIT` | 2 | `SQRT_DIGIT\|5\|root = 5` | manual_square_root_generator.py |
| `SQRT_NEG` | 2 | `SQRT_NEG\|√(-576)\|24i` | complex_quadratic_generator.py, polynomial_zeros_generator.py |
| `SQRT_SETUP` | 2 | `SQRT_SETUP\|N = 157\|x0 = 30` | manual_square_root_generator.py |
| `SQRT_TRIAL` | 3 | `SQRT_TRIAL\|x = 5\|(0 + 5)*5 = 25\|fits` | manual_square_root_generator.py |
| `SQUARE_BOTH_SIDES` | 2 | `SQUARE_BOTH_SIDES\|√(x + 28) = x - 2\|x + 28 = (x - 2)^2` | radical_equation_generator.py |
| `SQUARE_FACTOR` | 3 | `SQUARE_FACTOR\|33536\|256 × 131\|256` | radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `SQUARE_TEST` | 3 | `SQUARE_TEST\|20\|4^2 = 16, 5^2 = 25\|not a perfect square` | discriminant_generator.py |
| `STABILITY` | 3 | `STABILITY\|y=-11\|left up, right down\|stable` | stability_generator.py |
| `STANDING_BOUNDARY` | 1 | `STANDING_BOUNDARY\|open-open pipe allows n=1,2,3,...` | standing_wave_generator.py |
| `STANDING_FORMULA` | 1 | `STANDING_FORMULA\|lambda=2L/n, f=v/lambda` | standing_wave_generator.py |
| `STANDING_SETUP` | 3 | `STANDING_SETUP\|open_pipe\|n=3\|L=2, v=240` | standing_wave_generator.py |
| `STATEMENT_EVAL` | 3 | `STATEMENT_EVAL\|Pia says at least one of Pia and Oona is a knight\|T\|consistent` | knights_knaves_generator.py |
| `STATICS_FORMULA` | 1 | `STATICS_FORMULA\|sum_tau_left=0 => RB*L=W*x` | statics_generator.py |
| `STATICS_SETUP` | 3 | `STATICS_SETUP\|supported_beam\|W=89, L=11\|x=1` | statics_generator.py |
| `STATIONARY` | 2 | `STATIONARY\|pi0=1/2\|pi1=1/2` | entropy_rate_markov_generator.py |
| `STAT_ABS_DEV` | 2 | `STAT_ABS_DEV\|13\|13` | statistics_generator.py |
| `STAT_AVERAGE` | 2 | `STAT_AVERAGE\|(35 + 56) / 2\|45.5` | statistics_generator.py |
| `STAT_COUNT` | 1 | `STAT_COUNT\|5` | statistics_generator.py |
| `STAT_DEVIATION` | 3 | `STAT_DEVIATION\|60\|47\|13` | statistics_generator.py |
| `STAT_DIVIDE` | 2 | `STAT_DIVIDE\|205 / 5\|41` | statistics_generator.py |
| `STAT_FREQUENCY` | 2 | `STAT_FREQUENCY\|21\|4` | statistics_generator.py |
| `STAT_MAD` | 3 | `STAT_MAD\|54\|6\|9` | statistics_generator.py |
| `STAT_MAX` | 1 | `STAT_MAX\|96` | statistics_generator.py |
| `STAT_MEAN` | 2 | `STAT_MEAN\|282 / 6\|47` | statistics_generator.py |
| `STAT_MIDDLE` | 2 | `STAT_MIDDLE\|position 5\|42` | statistics_generator.py |
| `STAT_MIN` | 1 | `STAT_MIN\|13` | statistics_generator.py |
| `STAT_MODE` | 2 | `STAT_MODE\|21 and 64\|4` | statistics_generator.py |
| `STAT_ORDER` | 1 | `STAT_ORDER\|20, 22, 35, 36, 42, 51, 51, 66, 92` | statistics_generator.py |
| `STAT_RANGE` | 2 | `STAT_RANGE\|96 - 13\|83` | statistics_generator.py |
| `STAT_SETUP` | 1 | `STAT_SETUP\|46, 44, 48, 50, 17` | statistics_generator.py |
| `STAT_SUM` | 2 | `STAT_SUM\|46 + 44 + 48 + 50 + 17\|205` | statistics_generator.py |
| `STD` | 1 | `STD\|6` | layer_norm_generator.py |
| `STEADY_EQUATION` | 2 | `STEADY_EQUATION\|pi0*pi01=pi1*pi10\|pi0+pi1=1` | markov_chain_generator.py |
| `STEPPING_STONE` | 2 | `STEPPING_STONE\|enter x21\|+x21 -x22 +x12 -x11` | transportation_generator.py |
| `STEREO_SETUP` | 3, 4 | `STEREO_SETUP\|plane_to_sphere\|u=7/5\|v=7` | stereographic_generator.py |
| `STIRLING_CELL` | 3 | `STIRLING_CELL\|S(1,1)\|1×0+1\|1` | set_counting_generator.py |
| `STMT_EVAL` | 3 | `STMT_EVAL\|p\|6 is prime\|F` | logical_connective_eval_generator.py |
| `STOICH_RATIO` | 2 | `STOICH_RATIO\|CaCO3->CO2\|1/1=1` | gas_stoichiometry_generator.py, stoichiometry_generator.py |
| `STOICH_SETUP` | 2, 3 | `STOICH_SETUP\|mass_to_volume\|CaCO3 -> CaO + CO2\|given=1300 g CaCO3, target=CO2` | stoichiometry_generator.py |
| `STRUCTURE_CONSTANT` | 3 | `STRUCTURE_CONSTANT\|epsilon_yzx\|1\|-90iJx` | structure_constant_generator.py |
| `STRUCTURE_SETUP` | 3 | `STRUCTURE_SETUP\|A=9Jy\|B=-10Jz\|epsilon_yzx=1` | structure_constant_generator.py |
| `SU3_SETUP` | 2 | `SU3_SETUP\|left=3\|right=3bar` | young_tableaux_generator.py |
| `SUBEXPR` | 2 | `SUBEXPR\|A ∪ B\|{c, d}` | probability_measure_generator.py, set_expression_generator.py, set_operations_generator.py |
| `SUBGROUP` | 2 | `SUBGROUP\|H={1, 19, 9, 39, 37, 43, 25, 35, 5, 7}\|size 10` | coset_generator.py |
| `SUBGROUP_ELEM` | 2 | `SUBGROUP_ELEM\|k=1\|3` | coset_generator.py, cyclic_group_generator.py |
| `SUBGROUP_START` | 2 | `SUBGROUP_START\|H=<19>\|identity 1` | coset_generator.py |
| `SUBPROOF_CLOSE` | 3 | `SUBPROOF_CLOSE\|→I\|lines 2–3\|j → s` | natural_deduction_generator.py |
| `SUBPROOF_OPEN` | 2 | `SUBPROOF_OPEN\|assume\|j` | natural_deduction_generator.py |
| `SUBSET_CHECK` | 3 | `SUBSET_CHECK\|{26}\|subset of A?\|yes` | set_membership_subset_generator.py |
| `SUBSET_SIZE` | 2 | `SUBSET_SIZE\|0\|∅` | set_operations_generator.py |
| `SUBST` | 2, 3 | `SUBST\|x\|-5\|2(-5)+4y+7` | arc_length_generator.py, chain_rule_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, evaluate_expression_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, implicit_diff_generator.py, integrating_factor_generator.py, legendre_construction_generator.py, lhopital_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, ode_substitution_generator.py, optimization_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, power_series_generator.py, recursive_explicit_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, second_order_ode_generator.py, separable_ode_generator.py, tangent_line_generator.py, taylor_series_generator.py, trig_equation_generator.py, u_substitution_generator.py, undetermined_coeff_generator.py |
| `SUBSTITUTE` | 2, 3 | `SUBSTITUTE\|p ∨ (q ∨ r)\|p := (j ∨ c) ∨ ¬k; q := m ∨ d; r := g ∨ b\|((j ∨ c) ∨ ¬k) ∨ ((m ∨ d) ∨ (g ∨ b))` | hilbert_axiom_derivation_generator.py, lambda_reduction_generator.py |
| `SUBSTITUTION` | 2 | `SUBSTITUTION\|y = vx\|dy/dx = v + x dv/dx` | ode_substitution_generator.py |
| `SUB_COL` | 3 | `SUB_COL\|col_1\|5-6-borrow0\|->9 (borrow_out 1)` | multi_digit_subtraction_generator.py |
| `SUM` | 2, 3 | `SUM\|20 + 16 + 26\|62` | bayesian_update_generator.py, experimental_probability_generator.py, likelihood_language_generator.py, method_of_moments_generator.py, mle_generator.py, random_digit_simulation_generator.py, regression_generator.py |
| `SUM_ORDER` | 2 | `SUM_ORDER\|Σ i^9\|n^10` | master_theorem_generator.py |
| `SUPPORT` | 2 | `SUPPORT\|0<=u+v<=44\|0<=u-v<=44` | rv_transform_generator.py |
| `SUPPORT_TERM` | 2 | `SUPPORT_TERM\|1\|(-8,0)` | svm_margin_generator.py |
| `SVM_SETUP` | 3 | `SVM_SETUP\|x1=(8,0),y1=-1,alpha1=1\|x2=(0,-15),y2=1,alpha2=1\|b=1,x=(4,2)` | svm_margin_generator.py |
| `SWAP` | 2 | `SWAP\|norm b2=5\|norm b1=34` | lll_reduction_generator.py |
| `SWAP_VARS` | 1 | `SWAP_VARS\|x = y^3 - 6` | inverse_function_generator.py |
| `SYMBOL_CODE` | 2 | `SYMBOL_CODE\|exponent 5\|)` | godel_numbering_generator.py |
| `SYMMETRIC_CHECK` | 3 | `SYMMETRIC_CHECK\|(2, 2)\|reverse (2, 2)\|present` | equivalence_relation_generator.py, relation_check_generator.py |
| `SYMMETRY` | 2 | `SYMMETRY\|odd function\|a0=0, a_n=0` | fourier_series_generator.py |
| `SYNDIV_SETUP` | 2 | `SYNDIV_SETUP\|2x^4 - 7x^3 + 3x^2 + 3x + 7\|r = 2` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYNDROME_CALC` | 2 | `SYNDROME_CALC\|s1=b1 xor b3 xor b5 xor b7\|1 xor 0 xor 0 xor 0=1` | hamming_code_generator.py |
| `SYNDROME_VALUE` | 2 | `SYNDROME_VALUE\|s1=1, s2=0, s4=0\|position=1` | hamming_code_generator.py |
| `SYN_DROP` | 1 | `SYN_DROP\|2` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_ROW` | 1 | `SYN_ROW\|2, -3, -3, -3, 1` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYS_ADD` | 1 | `SYS_ADD\|Add equations: 6x = -36` | systems_elimination_generator.py |
| `SYS_EQ_NEW` | 1 | `SYS_EQ_NEW\|New equation with x only` | systems_substitution_generator.py |
| `SYS_ISOLATE` | 2 | `SYS_ISOLATE\|Isolate x in Eq 1\|x = -y - 11` | systems_substitution_generator.py |
| `SYS_MULT` | 1 | `SYS_MULT\|Eq1 * 2, Eq2 * -1` | systems_elimination_generator.py |
| `SYS_REWRITE` | 2 | `SYS_REWRITE\|2x + 4y = 24\|4x - 4y = -60` | systems_elimination_generator.py |
| `SYS_SETUP` | 2 | `SYS_SETUP\|y = -4x + 2\|-2x + 4y = 8` | systems_elimination_generator.py, systems_substitution_generator.py |
| `SYS_SUBST` | 1 | `SYS_SUBST\|Substitute (-4x + 2) for y in Eq 2` | systems_substitution_generator.py |
| `SYS_SUBST_BACK` | 1 | `SYS_SUBST_BACK\|Substitute x=0 into Eq 1` | systems_elimination_generator.py, systems_substitution_generator.py |
| `TABLEAU` | 2, 3 | `TABLEAU\|initial\|s1: x + s1 = 6\|s2: y + s2 = 6` | simplex_generator.py |
| `TABLEAU_ROOT` | 1 | `TABLEAU_ROOT\|(¬e ∧ ¬b) ∨ ¬q` | semantic_tableau_generator.py |
| `TABLEAU_RULE` | 3 | `TABLEAU_RULE\|3 x 3bar\|box plus antibox gives adjoint plus singlet\|8 + 1` | young_tableaux_generator.py |
| `TABLE_CELL` | 2 | `TABLE_CELL\|format=print, genre=fiction\|44` | two_way_table_probability_generator.py |
| `TABLE_COMPARE` | 1, 2 | `TABLE_COMPARE\|differ\|x ∈ D, x ∈ H, x ∉ R` | foundations_critic_generator.py, set_identity_membership_table_generator.py |
| `TABLE_ENTRY` | 2 | `TABLE_ENTRY\|f(-2)\|-1` | euler_method_generator.py, function_table_generator.py, taylor_series_generator.py |
| `TABLE_LOOKUP` | 2 | `TABLE_LOOKUP\|g(5)\|-2` | de_moivre_generator.py, dot_product_generator.py, euler_formula_generator.py, function_evaluation_generator.py, lie_exponential_generator.py, normal_table_generator.py, pascal_triangle_generator.py, polar_parametric_generator.py, right_triangle_trig_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, unit_circle_generator.py |
| `TABLE_TOTAL` | 2 | `TABLE_TOTAL\|grand\|44 + 36 + 21 + 79 = 180` | two_way_table_probability_generator.py |
| `TALLY` | 2 | `TALLY\|amber\|33` | experimental_probability_generator.py |
| `TANGENT_PLANE` | 2 | `TANGENT_PLANE\|z = z0 + fx(x-a) + fy(y-b)\|z = 27 + 12*(x - 3) + 9*(y - 4)` | gradient_generator.py |
| `TARGET_STATE` | 2 | `TARGET_STATE\|J=1/2\|M=-1/2` | clebsch_gordan_generator.py |
| `TAYLOR_FORMULA` | 1 | `TAYLOR_FORMULA\|P_n(x) = Σ f^(k)(a)/k!·(x - a)^k` | taylor_series_generator.py |
| `TAYLOR_SETUP` | 2 | `TAYLOR_SETUP\|f(x) = 1/x, center a = 1\|Taylor polynomial of degree 2` | taylor_series_generator.py |
| `TELESCOPE_CANCEL` | 2 | `TELESCOPE_CANCEL\|survive first and last\|1/2 - 1/95` | telescoping_generator.py |
| `TELE_SETUP` | 1 | `TELE_SETUP\|Σ k=2..94 (1/k - 1/(k+1))` | telescoping_generator.py |
| `TEMP_SCALE` | 2 | `TEMP_SCALE\|z1/T\|ln(2)` | softmax_gradient_generator.py |
| `TENSOR_ENTRY` | 2 | `TENSOR_ENTRY\|S_11\|-1` | einstein_summation_generator.py, index_raising_generator.py |
| `TENSOR_RULE` | 1 | `TENSOR_RULE\|diag(a,b) tensor diag(c,d)=diag(ac,ad,bc,bd)` | tensor_product_generator.py |
| `TENSOR_SETUP` | 3 | `TENSOR_SETUP\|A=diag(-5,-5)\|B=diag(-1,-5)\|u=[1,-2], v=[-1,2]` | tensor_product_generator.py |
| `TENSOR_STATE` | 2 | `TENSOR_STATE\|u tensor v\|[-1,2,2,-4]` | tensor_product_generator.py |
| `TERM` | 2, 3 | `TERM\|4 makes\|(7/10)^4\|2401/10000` | binomial_probability_generator.py, random_digit_simulation_generator.py |
| `TERMS` | 1 | `TERMS\|y[0..4]=[1,15,225,3375,50625]` | z_transform_generator.py |
| `TEST_CHOOSE` | 2 | `TEST_CHOOSE\|direct comparison\|compare with Σ 1/n^2` | power_series_generator.py, series_convergence_generator.py |
| `TEST_STAT_FORMULA` | 1 | `TEST_STAT_FORMULA\|z = (p̂ - p0)/√(p0(1-p0)/n)` | hypothesis_test_generator.py, two_sample_test_generator.py |
| `TF_SETUP` | 3 | `TF_SETUP\|ode\|y''+14y'+45y=3x'+36x\|zero initial conditions` | transfer_function_generator.py |
| `THEOREM` | 1, 2 | `THEOREM\|quadratic formula\|t = (-b ± √(b^2 - 4ac))/(2a)` | angle_defect_generator.py, circle_angle_generator.py, gauss_bonnet_generator.py, geometric_mean_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py, quadratic_generator.py, rational_root_generator.py, remainder_factor_theorem_generator.py, series_convergence_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py |
| `THEOREM_REWRITE` | 2 | `THEOREM_REWRITE\|circulation\|double integral of Q_x - P_y` | vector_theorem_generator.py |
| `THEOREM_SETUP` | 3 | `THEOREM_SETUP\|Green\|F=<0, -2*x>\|rectangle 5 by 3` | vector_theorem_generator.py |
| `THETA` | 2 | `THETA\|min(16,16)\|16` | transportation_generator.py |
| `THROUGHPUT` | 2 | `THROUGHPUT\|tokens_per_second\|1525000000/9` | scaling_law_generator.py |
| `TIME_COMPONENT` | 2 | `TIME_COMPONENT\|k=1\|-i` | braket_generator.py |
| `TIME_DERIV` | 2 | `TIME_DERIV\|d/dt(m*L^2*thetadot)\|m*L^2*thetaddot` | lagrangian_generator.py |
| `TIME_EVOLVE` | 2 | `TIME_EVOLVE\|U psi\|[-i,1]` | braket_generator.py |
| `TM_CONFIG` | 4 | `TM_CONFIG\|step 0\|state=q0\|head=0\|tape=101` | turing_machine_trace_generator.py |
| `TM_HALT` | 2 | `TM_HALT\|step 4\|halted` | turing_machine_trace_generator.py |
| `TM_MOVE` | 3 | `TM_MOVE\|0\|R\|1` | turing_machine_trace_generator.py |
| `TM_READ` | 2 | `TM_READ\|head=0\|1` | turing_machine_trace_generator.py |
| `TM_RULE` | 2 | `TM_RULE\|q0,0\|q0,1,R` | turing_machine_trace_generator.py |
| `TM_SETUP` | 3 | `TM_SETUP\|binary_flip\|input=101\|limit=6` | turing_machine_trace_generator.py |
| `TM_WRITE` | 2 | `TM_WRITE\|head=0\|0` | turing_machine_trace_generator.py |
| `TOPO_AVAILABLE` | 1 | `TOPO_AVAILABLE\|A` | graph_traversal_generator.py |
| `TOPO_PICK` | 2 | `TOPO_PICK\|available {4, 18, 25}\|pick 4` | partial_order_generator.py |
| `TOPO_READY` | 1 | `TOPO_READY\|B` | graph_traversal_generator.py |
| `TOPO_SELECT` | 2 | `TOPO_SELECT\|A\|A` | graph_traversal_generator.py |
| `TOTIENT_RESULT` | 2 | `TOTIENT_RESULT\|phi(29)\|28` | totient_generator.py |
| `TRACE` | 2 | `TRACE\|4 - 3\|1` | ode_system_generator.py |
| `TRACE_ADD` | 4 | `TRACE_ADD\|gamma0gamma0\|(1,1)\|0 + 1\|1` | gamma_matrix_generator.py |
| `TRACE_ENTRY` | 2 | `TRACE_ENTRY\|(1,1)\|8i` | einstein_summation_generator.py, pauli_algebra_generator.py |
| `TRACE_EXPECT` | 1, 3 | `TRACE_EXPECT\|Tr(rho A)=p0*a+p1*b` | density_matrix_generator.py, gamma_matrix_generator.py |
| `TRACE_SUM` | 2 | `TRACE_SUM\|8i - 8i\|0` | pauli_algebra_generator.py |
| `TRANSFER` | 1 | `TRANSFER\|H(s)=(3s+36)/(s^2+14s+45)` | transfer_function_generator.py |
| `TRANSFORM_APPLY` | 2 | `TRANSFORM_APPLY\|(2(-3), 2(-7))\|(-6, -14)` | transformation_generator.py |
| `TRANSFORM_RULE` | 1 | `TRANSFORM_RULE\|(x, y) → (2x, 2y)` | transformation_generator.py |
| `TRANSFORM_SETUP` | 2, 3 | `TRANSFORM_SETUP\|P(-3, -7)\|dilation by factor 2 centered at the origin` | rv_transform_generator.py, transformation_generator.py |
| `TRANSIENT_FORMULA` | 1 | `TRANSIENT_FORMULA\|tau=L/R` | transient_circuit_generator.py |
| `TRANSIENT_SETUP` | 3 | `TRANSIENT_SETUP\|rl_rise\|R=5, L=25\|V=9, t=5` | transient_circuit_generator.py |
| `TRANSITIVE_CHECK` | 2, 3 | `TRANSITIVE_CHECK\|(2, 2) and (2, 2)\|need (2, 2)\|present` | equivalence_relation_generator.py, hereditarily_finite_set_generator.py, relation_check_generator.py |
| `TRANSLATE` | 2 | `TRANSLATE\|Some volunteer is diligent\|∃v (C(v) ∧ Y(v))` | quantifier_negation_generator.py |
| `TRANSPORT_SETUP` | 3 | `TRANSPORT_SETUP\|supply=(19,16)\|demand=(16,19)\|costs=(14,12;5,7)` | transportation_generator.py |
| `TREE_BRANCH` | 3 | `TREE_BRANCH\|SF\|5/12 × 2/7\|5/42` | tree_diagram_probability_generator.py |
| `TRIG_RATIO` | 2 | `TRIG_RATIO\|tan\|opposite/adjacent` | right_triangle_trig_generator.py |
| `TRIG_SETUP` | 2 | `TRIG_SETUP\|right triangle: opposite side = 261, adjacent side = 348; given tan 37° ≈ 0.75\|angle A` | right_triangle_trig_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `TRIG_VALUE` | 2, 3 | `TRIG_VALUE\|sin(lat1)=0\|sin(lat2)=0\|cos(dlon)=-1` | christoffel_generator.py, great_circle_generator.py, spherical_triangle_generator.py |
| `TRIPLE_EVAL` | 3 | `TRIPLE_EVAL\|z_part * r_part * angle\|4*50*32*2*pi\|12800*pi` | triple_integral_generator.py |
| `TRIPLE_SETUP` | 3 | `TRIPLE_SETUP\|integrand 4*z\|cylinder radius 8, height 10\|cylindrical` | triple_integral_generator.py |
| `TRI_ANGLE_SETUP` | 3 | `TRI_ANGLE_SETUP\|38\|61\|x` | angle_relationships_generator.py |
| `TRI_ANGLE_SOLVE` | 2 | `TRI_ANGLE_SOLVE\|x = 180 - 38 - 61\|81` | angle_relationships_generator.py |
| `TRI_ANGLE_SUM` | 1 | `TRI_ANGLE_SUM\|38 + 61 + x = 180` | angle_relationships_generator.py |
| `TRI_AREA_FORMULA` | 1 | `TRI_AREA_FORMULA\|Area = (1/2)·a·b·sin C` | triangle_area_sas_generator.py |
| `TRI_SETUP` | 2 | `TRI_SETUP\|45-45-90 triangle, leg = 277\|hypotenuse` | special_right_triangle_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py |
| `TRUNCATE` | 2 | `TRUNCATE\|rank=1\|discard=7` | low_rank_approx_generator.py |
| `TRUTH_ROW` | 1, 2 | `TRUTH_ROW\|row 1\|p=T, q=T` | argument_form_generator.py, boolean_algebra_generator.py, truth_table_generator.py |
| `TRY` | 1, 2, 3 | `TRY\|x = −22\|−23 < x ≤ −7 and x is even\|true` | cantor_pairing_generator.py, conditional_forms_generator.py, counterexample_search_generator.py, factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, polynomial_inequality_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py, set_builder_roster_generator.py, structure_isomorphism_generator.py |
| `TS_FACTOR` | 3 | `TS_FACTOR\|p-1=40\|q=5\|s=3` | tonelli_shanks_generator.py |
| `TS_INIT` | 4 | `TS_INIT\|m=3\|c=38\|t=40\|r=4` | tonelli_shanks_generator.py |
| `TS_LOOP` | 2 | `TS_LOOP\|i=1\|b=9` | tonelli_shanks_generator.py |
| `TS_NONRESIDUE` | 1 | `TS_NONRESIDUE\|3` | tonelli_shanks_generator.py |
| `TS_SETUP` | 2 | `TS_SETUP\|a=25\|p=41` | tonelli_shanks_generator.py |
| `TT_COLUMN` | 2 | `TT_COLUMN\|formula\|TTTT` | truth_table_generator.py |
| `TT_SETUP` | 2 | `TT_SETUP\|variables p, q\|4` | truth_table_generator.py |
| `TWIDDLE` | 1, 3 | `TWIDDLE\|W4=-i\|W4^2=-1\|W4^3=i` | dft_generator.py |
| `TWOS_SETUP` | 2 | `TWOS_SETUP\|8-bit two's complement\|offset = 2^8 = 256` | base_conversion_generator.py |
| `TYPE_ABS` | 2 | `TYPE_ABS\|lambda n\|d → d` | type_theory_generator.py |
| `TYPE_APP` | 3 | `TYPE_APP\|(z q)\|unify\|K` | type_theory_generator.py |
| `TYPE_ASSIGN` | 2 | `TYPE_ASSIGN\|z\|a` | type_theory_generator.py |
| `UB` | 2 | `UB\|{{a}, {a, h, r}}\|{{a, h, r}}` | partial_order_generator.py |
| `UC_GUESS` | 2 | `UC_GUESS\|exponential forcing\|y_p = Ae^(2x)` | undetermined_coeff_generator.py |
| `UC_POINT` | 2 | `UC_POINT\|0°\|(1, 0)` | unit_circle_generator.py |
| `UNCERTAINTY_SETUP` | 3 | `UNCERTAINTY_SETUP\|particle in a box\|L=1, hbar=1\|n=160` | uncertainty_generator.py |
| `UNFOLD` | 2 | `UNFOLD\|gcd(182, 139)\|gcd(139, 43)` | recursive_definition_unfold_generator.py |
| `UNIFY_BIND` | 3 | `UNIFY_BIND\|X\|b\|{X=b}` | unification_generator.py |
| `UNIFY_DECOMPOSE` | 2 | `UNIFY_DECOMPOSE\|f\|2 arguments` | unification_generator.py |
| `UNIFY_FAIL` | 1 | `UNIFY_FAIL\|occurs-check X in f(X)` | unification_generator.py |
| `UNIFY_PAIR` | 2 | `UNIFY_PAIR\|X\|f(X)` | unification_generator.py |
| `UNIFY_SETUP` | 3 | `UNIFY_SETUP\|X\|f(X)\|occurs-check` | unification_generator.py |
| `UNION_ELEMENT` | 2 | `UNION_ELEMENT\|{{∅}, {{∅}, {∅, {∅}}}, {∅, {{∅}}, {{{∅}}}}, {{{{∅}}}}}\|contributes {{∅}, {{∅}, {∅, {∅}}}, {∅, {{∅}}, {{{∅}}}}, {{{{∅}}}}}` | hereditarily_finite_set_generator.py |
| `UNIT_ATTACH` | 3 | `UNIT_ATTACH\|3\|m/s^2\|3 m/s^2` | cross_section_generator.py, kinematics_generator.py, physics_formula_generator.py |
| `UNIT_CONVERT` | 2 | `UNIT_CONVERT\|5 minutes\|300 seconds` | physics_formula_generator.py |
| `UNIT_NORMAL` | 2 | `UNIT_NORMAL\|T'(0)/norm T'(0)\|<-1, 0>` | curve_geometry_generator.py |
| `UNIT_RATE_DIV` | 3 | `UNIT_RATE_DIV\|40 minutes\|4\|10 minutes` | unit_rate_generator.py |
| `UNIT_RATE_PICK` | 2 | `UNIT_RATE_PICK\|1\|3` | unit_rate_generator.py |
| `UNIT_RATE_SETUP` | 3 | `UNIT_RATE_SETUP\|4\|laps\|40 minutes` | unit_rate_generator.py |
| `UNIT_RATE_TABLE` | 2 | `UNIT_RATE_TABLE\|1,3,10\|3,9,30` | unit_rate_generator.py |
| `UNIT_RULE` | 3 | `UNIT_RULE\|c=1\|m=E\|mass uses eV` | natural_units_generator.py |
| `UNIT_TANGENT` | 2 | `UNIT_TANGENT\|r'(0)/speed\|<0, 1>` | curve_geometry_generator.py |
| `UNLIKE_RADICALS` | 2 | `UNLIKE_RADICALS\|√11 ≠ √13\|unlike radicands — cannot combine` | radical_add_sub_generator.py |
| `UNPAIR` | 2 | `UNPAIR\|54154\|(130, 198)` | cantor_pairing_generator.py |
| `UNPAIRED` | 2 | `UNPAIRED\|neither\|∅` | one_to_one_correspondence_generator.py |
| `UNROLL` | 2 | `UNROLL\|9, -36, 144, -576\|geometric, r = -4` | recursive_explicit_generator.py |
| `UPDATE` | 2 | `UPDATE\|W1_11\|-1` | backprop_generator.py, kernel_perceptron_generator.py |
| `U_VECTOR` | 2 | `U_VECTOR\|u1 = A*v1/σ1\|[1/√2, 1/√2]` | svd_generator.py |
| `VA` | 1 | `VA\|x = 2` | rational_function_features_generator.py |
| `VALIDITY` | 2 | `VALIDITY\|invalid\|denying the antecedent` | argument_form_generator.py |
| `VALUE_FORMULA` | 1 | `VALUE_FORMULA\|v=(ad-bc)/(a-b-c+d)` | game_theory_generator.py |
| `VARIANCE` | 1, 2 | `VARIANCE\|Delta x^2\|1/12 - 1/(51200pi^2)` | layer_norm_generator.py, uncertainty_generator.py |
| `VAR_FORMULA` | 1 | `VAR_FORMULA\|Var(X) = Σ P(x)·(x - μ)^2` | expected_value_generator.py |
| `VAR_ROW` | 3 | `VAR_ROW\|0 - 0.8 = -0.8\|(-0.8)^2 = 0.64\|3/10·0.64 = 0.192` | expected_value_generator.py |
| `VECTOR_NORM` | 2 | `VECTOR_NORM\|A\|5` | embedding_similarity_generator.py |
| `VECTOR_SETUP` | 2 | `VECTOR_SETUP\|F(x,y) = <-4*x + 4*y, 2*x - 3*y>\|divergence and scalar curl` | div_curl_generator.py |
| `VEC_ENTRY` | 3 | `VEC_ENTRY\|(1)\|272 + (-625)*8\|-4728` | diagonalization_generator.py |
| `VEC_SETUP` | 2 | `VEC_SETUP\|v = ⟨-5, 0⟩\|magnitude` | dot_product_generator.py, vector_ops_generator.py |
| `VENN_MARK` | 2 | `VENN_MARK\|artists ∩ ¬farmers\|x2` | syllogism_generator.py |
| `VENN_REGION` | 2 | `VENN_REGION\|A ∩ B\|4` | venn_probability_generator.py |
| `VENN_SHADE` | 2 | `VENN_SHADE\|artists − bakers\|empty` | syllogism_generator.py |
| `VERIFY` | 2 | `VERIFY\|1\|ok` | error_spotting_generator.py, foundations_critic_generator.py |
| `VERTEX` | 1 | `VERTEX\|(5, -6)` | ellipse_features_generator.py, hyperbola_features_generator.py, lp_corner_generator.py, parabola_features_generator.py |
| `VERTEX_SOLVE` | 2 | `VERTEX_SOLVE\|x=0\|y=0` | lp_corner_generator.py |
| `VISIT` | 2 | `VISIT\|B\|B` | graph_traversal_generator.py |
| `VITERBI_BACKTRACE` | 2 | `VITERBI_BACKTRACE\|L->H->H\|27/512` | viterbi_generator.py |
| `VITERBI_CAND` | 3 | `VITERBI_CAND\|t=2,state=H\|from H\|9/128` | convolutional_code_viterbi_generator.py, viterbi_generator.py |
| `VITERBI_INIT` | 3 | `VITERBI_INIT\|H\|obs=B\|1/8` | viterbi_generator.py |
| `VITERBI_PICK` | 2, 3 | `VITERBI_PICK\|t=2,state=H\|from L\|3/32` | convolutional_code_viterbi_generator.py, viterbi_generator.py |
| `VOLUME` | 1 | `VOLUME\|200` | volume_rect_prism_generator.py |
| `VOLUME_SETUP` | 2 | `VOLUME_SETUP\|region between y = 201x (outer) and y = 201x^2 (inner) on [0, 1], about the x-axis\|washer method` | solid_revolution_generator.py |
| `VOL_BASE_AREA` | 2 | `VOL_BASE_AREA\|Base Area = (1/2) × 11 × 5\|27.5` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_CALCULATE` | 2 | `VOL_CALCULATE\|V = 7 × 11 × 7\|539` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_FORMULA` | 1 | `VOL_FORMULA\|V = l × w × h` | round_solids_generator.py, solid_revolution_generator.py, volume_3d_generator.py |
| `VOL_SETUP` | 2 | `VOL_SETUP\|rectangular_prism\|l=7, w=11, h=7` | volume_3d_generator.py |
| `VOP_FORM` | 2 | `VOP_FORM\|u1' = -y2*g/W\|-30/1 * e^(6x)` | variation_parameters_generator.py |
| `WALK_ENTRY` | 2 | `WALK_ENTRY\|A^2[2,1]\|1` | graph_counting_generator.py |
| `WALK_GOAL` | 2 | `WALK_GOAL\|length 2\|2 to 1` | graph_counting_generator.py |
| `WALK_TERM` | 3 | `WALK_TERM\|via 1\|A[2,1]*A[1,1]\|0` | graph_counting_generator.py |
| `WARSHALL_K` | 2 | `WARSHALL_K\|k=6\|0 0 0; 1 0 0; 0 1 0` | relation_closure_generator.py |
| `WAVE_FORMULA` | 1 | `WAVE_FORMULA\|1=N^2*integral_0^L (x/L)^(2k) dx` | wavefunction_generator.py |
| `WAVE_SETUP` | 3 | `WAVE_SETUP\|power_interval\|psi=N*(x/L)^8\|0<=x<=23` | wavefunction_generator.py |
| `WEEKDAY_SCAN` | 2, 3 | `WEEKDAY_SCAN\|index 1\|Tuesday` | calendar_arithmetic_generator.py |
| `WEIGHT` | 2 | `WEIGHT\|blue\|57/98` | complement_probability_generator.py, probability_axioms_finite_generator.py, probability_measure_generator.py |
| `WEIGHT_VECTOR` | 2 | `WEIGHT_VECTOR\|w\|(-8,-15)` | svm_margin_generator.py |
| `WIDTH_SETUP` | 3 | `WIDTH_SETUP\|combined\|Gamma_a=15, Gamma_b=5, Gamma_c=11,hbar=9\|target=BR_a,tau` | branching_ratio_generator.py |
| `WITNESS` | 2, 3 | `WITNESS\|n=2\|Prime(2)=T\|Odd(2)=F` | induction_verify_generator.py, peano_arithmetic_generator.py, quantifier_finite_domain_generator.py, quantifier_negation_generator.py |
| `WORK_DIFF` | 3 | `WORK_DIFF\|phi(end) - phi(start)\|30 - 0\|30` | line_integral_generator.py |
| `WRONSKIAN` | 2 | `WRONSKIAN\|y1*y2' - y1'*y2\|e^(-3x)` | variation_parameters_generator.py |
| `XOR` | 3 | `XOR\|control=1\|target=1\|0` | quantum_gate_generator.py |
| `YOUNG_SETUP` | 3 | `YOUNG_SETUP\|partition=[3,3,2,1,1]\|n=10\|group=S_10` | young_tableaux_generator.py |
| `Z` | 1 | `Z\|63 R84` | abacus_addition_generator.py, absolute_value_equation_generator.py, absolute_value_inequality_generator.py, ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, algorithm_trace_generator.py, angle_defect_generator.py, angle_measure_generator.py, angle_relationships_generator.py, annuity_generator.py, antiderivative_generator.py, arc_length_generator.py, arc_sector_generator.py, area_between_curves_generator.py, argument_form_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, attribute_sorting_generator.py, baby_step_giant_step_generator.py, backprop_generator.py, base_arithmetic_generator.py, base_conversion_generator.py, bayesian_update_generator.py, bch_generator.py, bec_channel_generator.py, binomial_probability_generator.py, bisection_generator.py, bitwise_ops_generator.py, black_scholes_generator.py, blackbody_generator.py, bond_pricing_generator.py, boolean_algebra_generator.py, braket_generator.py, branching_ratio_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, cantor_diagonal_generator.py, cantor_pairing_generator.py, cardinal_arithmetic_generator.py, casimir_force_generator.py, casimir_generator.py, cauchy_riemann_generator.py, cayley_table_generator.py, centroid_generator.py, chain_rule_generator.py, channel_capacity_generator.py, characteristic_vector_generator.py, chi_square_generator.py, cholesky_generator.py, christoffel_generator.py, circle_angle_generator.py, circle_equation_generator.py, circle_generator.py, classifier_metrics_generator.py, clebsch_gordan_generator.py, collision_generator.py, combinatory_logic_generator.py, commutator_generator.py, complement_probability_generator.py, completing_square_generator.py, complex_division_generator.py, complex_locus_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, compound_inequality_generator.py, compound_probability_generator.py, conditional_forms_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, conservation_law_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, contour_integral_generator.py, convolution_generator.py, convolutional_code_viterbi_generator.py, coset_generator.py, countability_bijection_generator.py, counterexample_search_generator.py, counting_classics_generator.py, counting_to_probability_generator.py, cramers_rule_generator.py, crc_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, curve_geometry_generator.py, cyclic_group_generator.py, cyk_parser_generator.py, de_moivre_generator.py, decimal_add_sub_generator.py, decimal_div_generator.py, decimal_mult_generator.py, dedekind_cut_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dfa_minimization_generator.py, dfa_simulation_generator.py, dft_generator.py, diagonalization_generator.py, diffie_hellman_generator.py, dijkstra_generator.py, dimensional_analysis_generator.py, direct_proof_algebra_generator.py, discriminant_generator.py, distance_formula_generator.py, div_curl_generator.py, divisibility_classification_generator.py, domain_range_generator.py, doppler_generator.py, dot_product_generator.py, double_integral_generator.py, dp_table_generator.py, dpll_trace_generator.py, ecdh_generator.py, ecdsa_generator.py, eigenvalue_generator.py, einstein_summation_generator.py, electrostatics_generator.py, ellipse_features_generator.py, elliptic_curve_finite_field_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, english_to_logic_generator.py, entropy_change_generator.py, entropy_generator.py, entropy_rate_markov_generator.py, equation_from_two_points_generator.py, equilibrium_ice_generator.py, equivalence_relation_generator.py, error_spotting_generator.py, euler_characteristic_generator.py, euler_circuit_generator.py, euler_formula_generator.py, euler_method_generator.py, evaluate_expression_generator.py, exact_ode_generator.py, expected_value_generator.py, experimental_probability_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, exponential_model_generator.py, extended_euclid_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, factors_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, finite_difference_generator.py, finite_field_generator.py, first_law_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, foundations_critic_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_comparison_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_inner_product_generator.py, function_operations_generator.py, function_properties_generator.py, function_table_generator.py, fundamental_counting_principle_generator.py, fundamental_form_generator.py, game_theory_generator.py, gamma_matrix_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, gcf_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, godel_numbering_generator.py, gradient_descent_generator.py, gradient_generator.py, gradient_step_generator.py, gram_schmidt_generator.py, graph_counting_generator.py, graph_interpret_generator.py, graph_traversal_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, hamming_code_generator.py, hawking_generator.py, heat_engine_generator.py, hereditarily_finite_set_generator.py, hermitian_check_generator.py, hessian_classify_generator.py, hilbert_axiom_derivation_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, implicit_diff_generator.py, improper_integral_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, index_raising_generator.py, induction_verify_generator.py, information_gain_generator.py, integer_operations_generator.py, integers_as_pairs_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, inverse_function_generator.py, jacobi_symbol_generator.py, jacobian_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, knights_knaves_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrange_multiplier_generator.py, lagrangian_generator.py, lambda_reduction_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, least_squares_generator.py, legendre_construction_generator.py, lhopital_generator.py, lie_exponential_generator.py, likelihood_language_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, linear_simple_generator.py, literal_equation_generator.py, lll_reduction_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logic_grid_puzzle_generator.py, logical_connective_eval_generator.py, logical_equivalence_laws_generator.py, logistic_growth_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, lu_decomposition_generator.py, lz_compression_generator.py, magnetism_generator.py, manual_square_root_generator.py, markov_chain_generator.py, master_theorem_generator.py, matrix_calculus_generator.py, matrix_exponential_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_norm_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mle_generator.py, mobius_transform_generator.py, mod_exp_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, monomial_mult_div_generator.py, mst_generator.py, multi_digit_addition_generator.py, multi_digit_multiplication_generator.py, multi_digit_subtraction_generator.py, multi_step_unit_conversion_generator.py, multiplying_binomials_generator.py, multiplying_polynomials_generator.py, multivar_chain_rule_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_deduction_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, nfa_simulation_generator.py, normal_table_generator.py, npv_irr_generator.py, number_comparison_generator.py, odds_probability_generator.py, ode_substitution_generator.py, ode_system_generator.py, one_step_equation_generator.py, one_step_inequality_generator.py, one_to_one_correspondence_generator.py, operation_properties_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, ordinal_arithmetic_generator.py, parabola_features_generator.py, parallel_perpendicular_line_generator.py, param_count_generator.py, parametric_calculus_generator.py, partial_derivative_generator.py, partial_fractions_generator.py, partial_order_generator.py, partial_trace_generator.py, particle_in_box_generator.py, partition_function_generator.py, pascal_triangle_generator.py, pauli_algebra_generator.py, pca_generator.py, pda_simulation_generator.py, peano_arithmetic_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_combination_generator.py, permutation_group_generator.py, perplexity_generator.py, ph_calculation_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, place_value_rounding_generator.py, planck_units_generator.py, point_slope_generator.py, polar_parametric_generator.py, pollard_factorization_generator.py, polygon_perimeter_generator.py, polynomial_add_sub_generator.py, polynomial_div_monomial_generator.py, polynomial_inequality_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, positional_encoding_generator.py, positive_definite_generator.py, power_series_generator.py, prenex_normal_form_generator.py, primality_test_generator.py, prime_factorization_generator.py, probability_addition_rule_generator.py, probability_axioms_finite_generator.py, probability_measure_generator.py, projectile_motion_generator.py, projector_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, pythag_hyp_generator.py, pythag_leg_generator.py, qr_decomposition_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_residue_generator.py, quadratic_square_root_generator.py, quantifier_finite_domain_generator.py, quantifier_negation_generator.py, quantization_generator.py, quantum_formula_generator.py, quantum_gate_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, random_digit_simulation_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, rational_root_generator.py, rationals_as_pairs_generator.py, recurrence_generator.py, recursive_definition_unfold_generator.py, recursive_explicit_generator.py, reed_solomon_generator.py, regex_to_automaton_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, relation_check_generator.py, relation_closure_generator.py, relation_operations_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, repeating_decimal_generator.py, residue_generator.py, resolution_proof_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, sample_space_list_generator.py, scaling_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, semantic_tableau_generator.py, separable_ode_generator.py, separable_pde_generator.py, series_convergence_generator.py, series_solution_generator.py, set_algebra_laws_generator.py, set_builder_roster_generator.py, set_counting_generator.py, set_expression_generator.py, set_identity_membership_table_generator.py, set_membership_subset_generator.py, set_operations_generator.py, shm_generator.py, sigma_notation_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simple_stats_generator.py, simplex_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, slope_intercept_form_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solid_revolution_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, stability_generator.py, standard_deviation_generator.py, standard_form_conversion_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, statistics_generator.py, stereographic_generator.py, stoichiometry_generator.py, structure_constant_generator.py, structure_isomorphism_generator.py, subspace_basis_generator.py, svd_generator.py, svm_margin_generator.py, syllogism_generator.py, synthetic_division_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, telescoping_generator.py, temperature_conversion_generator.py, tensor_product_generator.py, tip_bill_split_generator.py, tonelli_shanks_generator.py, totient_generator.py, transfer_function_generator.py, transformation_generator.py, transient_circuit_generator.py, transportation_generator.py, tree_diagram_probability_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, triple_integral_generator.py, truth_table_generator.py, turing_machine_trace_generator.py, two_sample_test_generator.py, two_step_equation_generator.py, two_step_inequality_generator.py, two_way_table_probability_generator.py, type_theory_generator.py, u_substitution_generator.py, uncertainty_generator.py, undetermined_coeff_generator.py, unification_generator.py, unit_circle_generator.py, unit_conversion_generator.py, unit_rate_generator.py, variation_parameters_generator.py, vector_ops_generator.py, vector_theorem_generator.py, venn_probability_generator.py, venn_region_count_generator.py, viterbi_generator.py, volume_3d_generator.py, volume_rect_prism_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, wff_parsing_generator.py, young_tableaux_generator.py, z_score_generator.py, z_transform_generator.py, zf_axiom_identify_generator.py |
| `ZERO` | 1 | `ZERO\|s=-12` | transfer_function_generator.py |
| `ZERO_PRODUCT` | 2 | `ZERO_PRODUCT\|(x + 1)(x - 7)\|x = -1 or x = 7` | area_between_curves_generator.py, curve_analysis_generator.py, domain_range_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_inequality_generator.py, polynomial_zeros_generator.py, quadratic_factoring_generator.py, radical_equation_generator.py, trig_equation_generator.py |
| `ZSCORE` | 2 | `ZSCORE\|(100 - 82)/20\|0.9` | normal_table_generator.py, z_score_generator.py |
| `ZSCORE_FORMULA` | 1 | `ZSCORE_FORMULA\|z = (x - μ)/σ` | z_score_generator.py |
| `ZT_PAIR` | 1 | `ZT_PAIR\|Z{r^n u[n]}=1/(1-r z^-1)` | z_transform_generator.py |
| `ZT_SETUP` | 2, 3 | `ZT_SETUP\|difference\|y[n]-15y[n-1]=delta[n]\|y[-1]=0` | z_transform_generator.py |
