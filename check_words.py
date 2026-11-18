from build_ch1 import get_ch1_content
from build_ch2 import get_ch2_content
from build_ch3 import get_ch3_content
from build_ch4 import get_ch4_content
from build_ch5 import get_ch5_content
from build_ch6 import get_ch6_content
from build_ch7 import get_ch7_content
from build_ch8_refs import get_ch8_refs_content

chs = [
    ('Ch1', get_ch1_content()),
    ('Ch2', get_ch2_content()),
    ('Ch3', get_ch3_content()),
    ('Ch4', get_ch4_content()),
    ('Ch5', get_ch5_content()),
    ('Ch6', get_ch6_content()),
    ('Ch7', get_ch7_content()),
    ('Ch8+Ref', get_ch8_refs_content())
]

total = 0
for name, txt in chs:
    w = len(txt.split())
    total += w
    print(f"{name}: {w} words")
print(f"Total Body Words: {total}")
