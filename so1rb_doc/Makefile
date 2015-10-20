ALL = EXPLORATION.html SOLUTION.html

.PHONY: all clean

all: $(ALL)

clean:
	$(RM) -f $(ALL)

EXPLORATION.html: EXPLORATION.md
	pandoc -S -s --mathjax -t slidy --template myslidy.html EXPLORATION.md -o EXPLORATION.html

SOLUTION.html: SOLUTION.md
	pandoc -S -s --mathjax SOLUTION.md -o SOLUTION.html
