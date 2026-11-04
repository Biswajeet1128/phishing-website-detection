/**
 * Embedded Model Data for Chrome Extension
 * AI-Based Phishing Website Detection System
 */
const MODEL_DATA = {
  "model_type": "DecisionTreeClassifier",
  "track": "Model B (URL Real-Time)",
  "target_classes": [
    0,
    1
  ],
  "class_names": [
    "Legitimate",
    "Phishing"
  ],
  "feature_names": [
    "having_IP_Address",
    "URL_Length",
    "Shortining_Service",
    "having_At_Symbol",
    "double_slash_redirecting",
    "Prefix_Suffix",
    "having_Sub_Domain",
    "HTTPS_token"
  ],
  "num_features": 8,
  "tree": {
    "node_id": 0,
    "is_leaf": false,
    "samples": 1,
    "class_counts": [
      0.5569877883310719,
      0.44301221166892807
    ],
    "probabilities": [
      0.557,
      0.443
    ],
    "predicted_class": 0,
    "predicted_label": "Legitimate",
    "feature_index": 5,
    "feature_name": "Prefix_Suffix",
    "threshold": 0.0,
    "left": {
      "node_id": 1,
      "is_leaf": false,
      "samples": 1,
      "class_counts": [
        0.49077203015336623,
        0.5092279698466338
      ],
      "probabilities": [
        0.4908,
        0.5092
      ],
      "predicted_class": 1,
      "predicted_label": "Phishing",
      "feature_index": 6,
      "feature_name": "having_Sub_Domain",
      "threshold": 0.5,
      "left": {
        "node_id": 2,
        "is_leaf": false,
        "samples": 1,
        "class_counts": [
          0.35063643595863164,
          0.6493635640413683
        ],
        "probabilities": [
          0.3506,
          0.6494
        ],
        "predicted_class": 1,
        "predicted_label": "Phishing",
        "feature_index": 0,
        "feature_name": "having_IP_Address",
        "threshold": 0.0,
        "left": {
          "node_id": 3,
          "is_leaf": false,
          "samples": 1,
          "class_counts": [
            0.26932223543400713,
            0.7306777645659929
          ],
          "probabilities": [
            0.2693,
            0.7307
          ],
          "predicted_class": 1,
          "predicted_label": "Phishing",
          "feature_index": 2,
          "feature_name": "Shortining_Service",
          "threshold": 0.0,
          "left": {
            "node_id": 4,
            "is_leaf": false,
            "samples": 1,
            "class_counts": [
              0.42535787321063395,
              0.5746421267893661
            ],
            "probabilities": [
              0.4254,
              0.5746
            ],
            "predicted_class": 1,
            "predicted_label": "Phishing",
            "feature_index": 3,
            "feature_name": "having_At_Symbol",
            "threshold": 0.0,
            "left": {
              "node_id": 5,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.25196850393700787,
                0.7480314960629921
              ],
              "probabilities": [
                0.252,
                0.748
              ],
              "predicted_class": 1,
              "predicted_label": "Phishing",
              "feature_index": 1,
              "feature_name": "URL_Length",
              "threshold": -0.5,
              "left": {
                "node_id": 6,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.20238095238095238,
                  0.7976190476190477
                ],
                "probabilities": [
                  0.2024,
                  0.7976
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              },
              "right": {
                "node_id": 7,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.3488372093023256,
                  0.6511627906976745
                ],
                "probabilities": [
                  0.3488,
                  0.6512
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              }
            },
            "right": {
              "node_id": 8,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.4861878453038674,
                0.5138121546961326
              ],
              "probabilities": [
                0.4862,
                0.5138
              ],
              "predicted_class": 1,
              "predicted_label": "Phishing",
              "feature_index": 6,
              "feature_name": "having_Sub_Domain",
              "threshold": -0.5,
              "left": {
                "node_id": 9,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.6054421768707483,
                  0.3945578231292517
                ],
                "probabilities": [
                  0.6054,
                  0.3946
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              },
              "right": {
                "node_id": 10,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.4046511627906977,
                  0.5953488372093023
                ],
                "probabilities": [
                  0.4047,
                  0.5953
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              }
            }
          },
          "right": {
            "node_id": 11,
            "is_leaf": false,
            "samples": 1,
            "class_counts": [
              0.20536462699077954,
              0.7946353730092205
            ],
            "probabilities": [
              0.2054,
              0.7946
            ],
            "predicted_class": 1,
            "predicted_label": "Phishing",
            "feature_index": 6,
            "feature_name": "having_Sub_Domain",
            "threshold": -0.5,
            "left": {
              "node_id": 12,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.2847682119205298,
                0.7152317880794702
              ],
              "probabilities": [
                0.2848,
                0.7152
              ],
              "predicted_class": 1,
              "predicted_label": "Phishing",
              "feature_index": 4,
              "feature_name": "double_slash_redirecting",
              "threshold": 0.0,
              "left": {
                "node_id": 13,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.0,
                  1.0
                ],
                "probabilities": [
                  0.0,
                  1.0
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              },
              "right": {
                "node_id": 14,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.2945205479452055,
                  0.7054794520547946
                ],
                "probabilities": [
                  0.2945,
                  0.7055
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              }
            },
            "right": {
              "node_id": 15,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.15675675675675677,
                0.8432432432432433
              ],
              "probabilities": [
                0.1568,
                0.8432
              ],
              "predicted_class": 1,
              "predicted_label": "Phishing",
              "feature_index": 7,
              "feature_name": "HTTPS_token",
              "threshold": 0.0,
              "left": {
                "node_id": 16,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.019230769230769232,
                  0.9807692307692307
                ],
                "probabilities": [
                  0.0192,
                  0.9808
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              },
              "right": {
                "node_id": 17,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.16715116279069767,
                  0.8328488372093024
                ],
                "probabilities": [
                  0.1672,
                  0.8328
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              }
            }
          }
        },
        "right": {
          "node_id": 18,
          "is_leaf": false,
          "samples": 1,
          "class_counts": [
            0.39151225343693963,
            0.6084877465630604
          ],
          "probabilities": [
            0.3915,
            0.6085
          ],
          "predicted_class": 1,
          "predicted_label": "Phishing",
          "feature_index": 1,
          "feature_name": "URL_Length",
          "threshold": 0.5,
          "left": {
            "node_id": 19,
            "is_leaf": false,
            "samples": 1,
            "class_counts": [
              0.36916548797736914,
              0.6308345120226309
            ],
            "probabilities": [
              0.3692,
              0.6308
            ],
            "predicted_class": 1,
            "predicted_label": "Phishing",
            "feature_index": 2,
            "feature_name": "Shortining_Service",
            "threshold": 0.0,
            "left": {
              "node_id": 20,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.5866666666666667,
                0.41333333333333333
              ],
              "probabilities": [
                0.5867,
                0.4133
              ],
              "predicted_class": 0,
              "predicted_label": "Legitimate",
              "feature_index": 4,
              "feature_name": "double_slash_redirecting",
              "threshold": 0.0,
              "left": {
                "node_id": 21,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.34285714285714286,
                  0.6571428571428571
                ],
                "probabilities": [
                  0.3429,
                  0.6571
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              },
              "right": {
                "node_id": 22,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.8,
                  0.2
                ],
                "probabilities": [
                  0.8,
                  0.2
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              }
            },
            "right": {
              "node_id": 23,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.3632401017072285,
                0.6367598982927716
              ],
              "probabilities": [
                0.3632,
                0.6368
              ],
              "predicted_class": 1,
              "predicted_label": "Phishing",
              "feature_index": 4,
              "feature_name": "double_slash_redirecting",
              "threshold": 0.0,
              "left": {
                "node_id": 24,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.02702702702702703,
                  0.972972972972973
                ],
                "probabilities": [
                  0.027,
                  0.973
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              },
              "right": {
                "node_id": 25,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.36782032400589104,
                  0.632179675994109
                ],
                "probabilities": [
                  0.3678,
                  0.6322
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              }
            }
          },
          "right": {
            "node_id": 26,
            "is_leaf": false,
            "samples": 1,
            "class_counts": [
              0.5135135135135135,
              0.4864864864864865
            ],
            "probabilities": [
              0.5135,
              0.4865
            ],
            "predicted_class": 0,
            "predicted_label": "Legitimate",
            "feature_index": 2,
            "feature_name": "Shortining_Service",
            "threshold": 0.0,
            "left": {
              "node_id": 27,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.23076923076923078,
                0.7692307692307693
              ],
              "probabilities": [
                0.2308,
                0.7692
              ],
              "predicted_class": 1,
              "predicted_label": "Phishing",
              "feature_index": 3,
              "feature_name": "having_At_Symbol",
              "threshold": 0.0,
              "left": {
                "node_id": 28,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.6666666666666666,
                  0.3333333333333333
                ],
                "probabilities": [
                  0.6667,
                  0.3333
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              },
              "right": {
                "node_id": 29,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.1,
                  0.9
                ],
                "probabilities": [
                  0.1,
                  0.9
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              }
            },
            "right": {
              "node_id": 30,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.5207920792079208,
                0.4792079207920792
              ],
              "probabilities": [
                0.5208,
                0.4792
              ],
              "predicted_class": 0,
              "predicted_label": "Legitimate",
              "feature_index": 7,
              "feature_name": "HTTPS_token",
              "threshold": 0.0,
              "left": {
                "node_id": 31,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.7272727272727273,
                  0.2727272727272727
                ],
                "probabilities": [
                  0.7273,
                  0.2727
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              },
              "right": {
                "node_id": 32,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.5113871635610766,
                  0.4886128364389234
                ],
                "probabilities": [
                  0.5114,
                  0.4886
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              }
            }
          }
        }
      },
      "right": {
        "node_id": 33,
        "is_leaf": false,
        "samples": 1,
        "class_counts": [
          0.7550637659414854,
          0.24493623405851464
        ],
        "probabilities": [
          0.7551,
          0.2449
        ],
        "predicted_class": 0,
        "predicted_label": "Legitimate",
        "feature_index": 0,
        "feature_name": "having_IP_Address",
        "threshold": 0.0,
        "left": {
          "node_id": 34,
          "is_leaf": false,
          "samples": 1,
          "class_counts": [
            0.6750272628135223,
            0.3249727371864776
          ],
          "probabilities": [
            0.675,
            0.325
          ],
          "predicted_class": 0,
          "predicted_label": "Legitimate",
          "feature_index": 2,
          "feature_name": "Shortining_Service",
          "threshold": 0.0,
          "left": {
            "node_id": 35,
            "is_leaf": false,
            "samples": 1,
            "class_counts": [
              0.7360594795539034,
              0.26394052044609667
            ],
            "probabilities": [
              0.7361,
              0.2639
            ],
            "predicted_class": 0,
            "predicted_label": "Legitimate",
            "feature_index": 1,
            "feature_name": "URL_Length",
            "threshold": 0.5,
            "left": {
              "node_id": 36,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.8391959798994975,
                0.16080402010050251
              ],
              "probabilities": [
                0.8392,
                0.1608
              ],
              "predicted_class": 0,
              "predicted_label": "Legitimate",
              "feature_index": 3,
              "feature_name": "having_At_Symbol",
              "threshold": 0.0,
              "left": {
                "node_id": 37,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.5918367346938775,
                  0.40816326530612246
                ],
                "probabilities": [
                  0.5918,
                  0.4082
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              },
              "right": {
                "node_id": 38,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.92,
                  0.08
                ],
                "probabilities": [
                  0.92,
                  0.08
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              }
            },
            "right": {
              "node_id": 39,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.44285714285714284,
                0.5571428571428572
              ],
              "probabilities": [
                0.4429,
                0.5571
              ],
              "predicted_class": 1,
              "predicted_label": "Phishing",
              "feature_index": 7,
              "feature_name": "HTTPS_token",
              "threshold": 0.0,
              "left": {
                "node_id": 40,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.45588235294117646,
                  0.5441176470588235
                ],
                "probabilities": [
                  0.4559,
                  0.5441
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              },
              "right": {
                "node_id": 41,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.0,
                  1.0
                ],
                "probabilities": [
                  0.0,
                  1.0
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              }
            }
          },
          "right": {
            "node_id": 42,
            "is_leaf": false,
            "samples": 1,
            "class_counts": [
              0.6496913580246914,
              0.35030864197530864
            ],
            "probabilities": [
              0.6497,
              0.3503
            ],
            "predicted_class": 0,
            "predicted_label": "Legitimate",
            "feature_index": 4,
            "feature_name": "double_slash_redirecting",
            "threshold": 0.0,
            "left": {
              "node_id": 43,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.3125,
                0.6875
              ],
              "probabilities": [
                0.3125,
                0.6875
              ],
              "predicted_class": 1,
              "predicted_label": "Phishing",
              "feature_index": 3,
              "feature_name": "having_At_Symbol",
              "threshold": 0.0,
              "left": {
                "node_id": 44,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.0,
                  1.0
                ],
                "probabilities": [
                  0.0,
                  1.0
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              },
              "right": {
                "node_id": 45,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.5,
                  0.5
                ],
                "probabilities": [
                  0.5,
                  0.5
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              }
            },
            "right": {
              "node_id": 46,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.6582278481012658,
                0.34177215189873417
              ],
              "probabilities": [
                0.6582,
                0.3418
              ],
              "predicted_class": 0,
              "predicted_label": "Legitimate",
              "feature_index": 1,
              "feature_name": "URL_Length",
              "threshold": 0.5,
              "left": {
                "node_id": 47,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.6393129770992366,
                  0.3606870229007634
                ],
                "probabilities": [
                  0.6393,
                  0.3607
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              },
              "right": {
                "node_id": 48,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.75,
                  0.25
                ],
                "probabilities": [
                  0.75,
                  0.25
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              }
            }
          }
        },
        "right": {
          "node_id": 49,
          "is_leaf": false,
          "samples": 1,
          "class_counts": [
            0.7970268724985706,
            0.2029731275014294
          ],
          "probabilities": [
            0.797,
            0.203
          ],
          "predicted_class": 0,
          "predicted_label": "Legitimate",
          "feature_index": 1,
          "feature_name": "URL_Length",
          "threshold": -0.5,
          "left": {
            "node_id": 50,
            "is_leaf": false,
            "samples": 1,
            "class_counts": [
              0.7779291553133515,
              0.2220708446866485
            ],
            "probabilities": [
              0.7779,
              0.2221
            ],
            "predicted_class": 0,
            "predicted_label": "Legitimate",
            "feature_index": 7,
            "feature_name": "HTTPS_token",
            "threshold": 0.0,
            "left": {
              "node_id": 51,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.6666666666666666,
                0.3333333333333333
              ],
              "probabilities": [
                0.6667,
                0.3333
              ],
              "predicted_class": 0,
              "predicted_label": "Legitimate",
              "feature_index": 2,
              "feature_name": "Shortining_Service",
              "threshold": 0.0,
              "left": {
                "node_id": 52,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.8387096774193549,
                  0.16129032258064516
                ],
                "probabilities": [
                  0.8387,
                  0.1613
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              },
              "right": {
                "node_id": 53,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.56,
                  0.44
                ],
                "probabilities": [
                  0.56,
                  0.44
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              }
            },
            "right": {
              "node_id": 54,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.7844268204758471,
                0.21557317952415284
              ],
              "probabilities": [
                0.7844,
                0.2156
              ],
              "predicted_class": 0,
              "predicted_label": "Legitimate",
              "feature_index": 3,
              "feature_name": "having_At_Symbol",
              "threshold": 0.0,
              "left": {
                "node_id": 55,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.8062015503875969,
                  0.1937984496124031
                ],
                "probabilities": [
                  0.8062,
                  0.1938
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              },
              "right": {
                "node_id": 56,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.7821939586645469,
                  0.2178060413354531
                ],
                "probabilities": [
                  0.7822,
                  0.2178
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              }
            }
          },
          "right": {
            "node_id": 57,
            "is_leaf": false,
            "samples": 1,
            "class_counts": [
              0.896797153024911,
              0.10320284697508897
            ],
            "probabilities": [
              0.8968,
              0.1032
            ],
            "predicted_class": 0,
            "predicted_label": "Legitimate",
            "feature_index": 2,
            "feature_name": "Shortining_Service",
            "threshold": 0.0,
            "left": {
              "node_id": 58,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.6,
                0.4
              ],
              "probabilities": [
                0.6,
                0.4
              ],
              "predicted_class": 0,
              "predicted_label": "Legitimate",
              "feature_index": 1,
              "feature_name": "URL_Length",
              "threshold": 0.5,
              "left": {
                "node_id": 59,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  1.0,
                  0.0
                ],
                "probabilities": [
                  1.0,
                  0.0
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              },
              "right": {
                "node_id": 60,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.3333333333333333,
                  0.6666666666666666
                ],
                "probabilities": [
                  0.3333,
                  0.6667
                ],
                "predicted_class": 1,
                "predicted_label": "Phishing"
              }
            },
            "right": {
              "node_id": 61,
              "is_leaf": false,
              "samples": 1,
              "class_counts": [
                0.9195402298850575,
                0.08045977011494253
              ],
              "probabilities": [
                0.9195,
                0.0805
              ],
              "predicted_class": 0,
              "predicted_label": "Legitimate",
              "feature_index": 3,
              "feature_name": "having_At_Symbol",
              "threshold": 0.0,
              "left": {
                "node_id": 62,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.8260869565217391,
                  0.17391304347826086
                ],
                "probabilities": [
                  0.8261,
                  0.1739
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              },
              "right": {
                "node_id": 63,
                "is_leaf": true,
                "samples": 1,
                "class_counts": [
                  0.9395348837209302,
                  0.06046511627906977
                ],
                "probabilities": [
                  0.9395,
                  0.0605
                ],
                "predicted_class": 0,
                "predicted_label": "Legitimate"
              }
            }
          }
        }
      }
    },
    "right": {
      "node_id": 64,
      "is_leaf": true,
      "samples": 1,
      "class_counts": [
        1.0,
        0.0
      ],
      "probabilities": [
        1.0,
        0.0
      ],
      "predicted_class": 0,
      "predicted_label": "Legitimate"
    }
  },
  "threshold": 0.5,
  "metadata": {
    "criterion": "entropy",
    "max_depth": 6,
    "n_classes": 2,
    "n_features": 8
  }
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = MODEL_DATA;
}
