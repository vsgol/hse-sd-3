from string_processor import StringProcessor

code = 'test = asf | echo 1'
code1 = 'test asf | pwd c:/src/test.a'
processor = StringProcessor()
res = processor.process(code1, {})
print(res)
