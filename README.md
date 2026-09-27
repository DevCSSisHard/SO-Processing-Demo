# Steel Price Estimator (demo)

A small catalog-driven price estimator: pick a category, pick an item, enter
quantity and length, get a predicted $/lb and line total.

This is a **showcase repo**; the API here (`api.py`) mirrors the full
service's routes, auth, and CORS setup, but runs on inline sample data with a
fixed placeholder price instead of the actual trained pricing model. The full
catalog and model logic are kept in a private repo.

## Structure - Work in Progress

- `web/index.html` — static frontend, no build step
- `api.py` backend: `/api/categories`, `/api/items`, `/api/predict`

  ## How the price estimate works

  The model learns from past invoices from three steel vendors and predicts a $/lb
  price for any item in the catalog, based on its shape, size, quantity, and weight.

  ### 1. Recent prices count more

  Steel prices change over time, so a quote from last month matters more than one
  from two years ago. Each past invoice is given a weight based on its age: the weight
  is cut in half for every 9 months of age. "Half-Life" weight approach.

  | Invoice age | How much it counts |
  |---|---|
  | Newest       | 100% |
  | 9 months     | 50%  |
  | 18 months    | 25%  |
  | 3 years      | ~6%  |

  Older invoices still help the model learn how size, shape, and quantity affect
  price. They just have less say in the overall price level. The model is retrained
  a few times a year as new invoices & quotes are collected.

  ### 2. Compare vendors, drop the outlier

  For every estimate, the model predicts what **each vendor** would charge, then
  combines them:

  1. Predict a price for Vendor A, Vendor B, and Vendor C.
  2. Find the middle (median) price.
  3. Drop any vendor more than 25% away from that middle price.
  4. Average the vendors that are left.

  **Example: 1/4" x 2" flat bar**

  | Vendor | Predicted $/lb | Result |
  |---|---|---|
  | Vendor A | $0.89 | kept |
  | Vendor B | $1.60 | dropped (80% above the middle) |
  | Vendor C | $0.88 | kept |
  | **Estimate** | **$0.885** | average of A and C |

  Without this step, the plain average would be $1.12/lb, about 25% too high.
  Outliers like this are common because some vendors specialize in heavy material
  (beams, plate) and charge much more on small items. On heavy items, where the same
  vendor is competitive, their price stays in the average. This approach is scalable with any number of vendors as well.

  ### Accuracy

  Checked against recent real purchases, the estimates landed within about 5% of the
  actual invoice total. The tool is meant for quick project estimates, not exact quotes.
