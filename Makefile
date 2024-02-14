test:
	pytest

build: $(subst src/,target/,$(wildcard src/*.py)) target/index_html_tpl.py target/style_css_tpl.py

target/%.py: src/%.py | target
	cp $< $@

target/style_css_tpl.py: templates/style.css.tpl
	python ../utemplate/utemplate_util.py rawcompile templates/style.css.tpl
	cp templates/style_css_tpl.py target/style_css_tpl.py
	rm templates/style_css_tpl.py

target/index_html_tpl.py: templates/index.html.tpl
	python ../utemplate/utemplate_util.py rawcompile templates/index.html.tpl
	cp templates/index_html_tpl.py target/index_html_tpl.py
	rm templates/index_html_tpl.py

target:
	mkdir -p $@
	
clean:
	rm -rf target
