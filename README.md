# Break-even Location Finder

Find the cheapest alternative at every volume, and the break-even quantities between alternatives, without drawing a graph.

The tool solves locational break-even analysis (also used for process selection and make-or-buy decisions). Each alternative has a fixed cost (FC) and a variable cost per unit (VC):

```
TC = FC + VC × Q
Q* = (FC₂ − FC₁) / (VC₁ − VC₂)
```

## Contents

| File | Purpose |
|---|---|
| `index.html` | Web app, English and Arabic. Open in any browser, no install. |
| `break_even_envelope.py` | Python implementation with a command line interface. |
| `test_break_even.py` | Tests against brute force on 5,000 random cases. |
| `example.csv` | Fall-Line, Inc. example data. |

## Web app

Open `index.html` in a browser, or enable GitHub Pages for this repository (Settings, Pages, deploy from the `main` branch).

Features:

- Enter name, fixed cost, and variable cost for any number of alternatives.
- Chart of all total cost lines. Thick segments mark the cheapest alternative. Dots mark each Q*.
- Table of winning ranges and break-even quantities.
- Step-by-step trace of the algorithm for teaching.
- Hover or tap the chart to compare costs at any volume.
- English and Arabic interface (العربية) with right-to-left layout. Open `index.html?lang=ar` to start in Arabic.

## Python

```
python break_even_envelope.py                    # Fall-Line example
python break_even_envelope.py example.csv --unit pairs
python test_break_even.py
```

CSV format:

```
name,fc,vc
Aspen,8000000,250
Boyne City,2400000,130
```

No external packages needed. Python 3.8 or later.

## Algorithm

Input: FC and VC for n alternatives. Output: the minimal lines in order of volume, and Q* between them.

1. Sort alternatives by VC from highest to lowest. For equal VC, put the lower FC first.
2. Scan with a stack. For each alternative k:
   - If VC equals the VC of the top line, skip k.
   - While FC of k ≤ FC of the top line, pop the top (dominated).
   - While the stack holds 2 or more lines, let j be the top and i the line below. If Q*(i, k) ≤ Q*(i, j), pop j. Line k overtakes i before j does, so j never wins.
   - Push k.
3. The stack holds the minimal lines from low to high volume. Q* between consecutive lines gives the range boundaries.

Running time: O(n log n) for the sort, O(n) for the scan.

The method computes the lower envelope of lines. In computational geometry, the same result follows from point-line duality and the convex hull. Plot each alternative as the point (VC, FC). Alternatives on the lower-left convex hull win a range, and minus the slope of each hull edge equals Q*.

## Example: Fall-Line, Inc.

| Location | FC | VC |
|---|---|---|
| Aspen | 8,000,000 | 250 |
| Boyne City | 2,400,000 | 130 |
| Portland | 3,400,000 | 90 |
| Lake Tahoe | 4,500,000 | 65 |

Result:

- Boyne City: 0 to 25,000 pairs
- Portland: 25,000 to 44,000 pairs
- Lake Tahoe: above 44,000 pairs
- Aspen: never cheapest

---

# أداة تحديد الموقع بتحليل نقطة التعادل

<div dir="rtl">

تحدد الأداة البديل الأقل تكلفة عند كل حجم إنتاج، وكميات التعادل بين البدائل، دون رسم بياني.

لكل بديل تكلفة ثابتة (FC) وتكلفة متغيرة للوحدة (VC). التكلفة الكلية: TC = FC + VC × Q

طريقة الاستخدام:

- افتح الملف `index.html` في المتصفح، واضغط زر "العربية" لتحويل الواجهة إلى العربية، أو افتح `index.html?lang=ar`.
- أدخل اسم كل بديل وتكلفته الثابتة والمتغيرة.
- تعرض الأداة الرسم البياني، ومدى الحجم الذي يكون فيه كل بديل الأفضل، وكميات التعادل، وخطوات الخوارزمية.

الخوارزمية:

1. رتّب البدائل حسب التكلفة المتغيرة من الأعلى إلى الأدنى.
2. امسح البدائل باستخدام مكدس، واحذف كل بديل مُهيمَن عليه أو لا يكون الأقل تكلفة في أي مدى.
3. البدائل المتبقية في المكدس هي البدائل الفائزة، ونقاط التعادل بينها تحدد حدود كل مدى.

</div>

## Author

Ramiz, Industrial Engineering Department, An-Najah National University.
