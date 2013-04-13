VERSION=0.3\(b2\)
LASTCHANGE=04\/14\/2013\ 00:00
BUILDTIME=$(shell date '+%m\/%d\/%Y\ %H:%M')


release: plugin/autocommand.vim
debug: plugin/autocommand.vim plugin/autocommand.py

plugin/autocommand.vim: src/autocommand.vim src/autocommand.py
	@cd plugin || mkdir plugin
	sed -n '1,40p' src/autocommand.vim > $@.tmp
	cat src/autocommand.py >> $@.tmp
	sed -n '42,126p' src/autocommand.vim >> $@.tmp
	sed -i 's/$$version\$$/$(VERSION)/g' $@.tmp
	sed -i 's/$$lastChange\$$/$(LASTCHANGE)/g' $@.tmp
	sed -i 's/$$buildTime\$$/$(BUILDTIME)/g' $@.tmp
	mv $@.tmp $@

plugin/autocommand.py: src/autocommand.py
	@cd plugin || mkdir plugin
	cp $< $@.tmp
	sed -i 's/$$version\$$/$(VERSION)/g' $@.tmp
	sed -i 's/$$lastChange\$$/$(LASTCHANGE)/g' $@.tmp
	sed -i 's/$$buildTime\$$/$(BUILDTIME)/g' $@.tmp
	mv $@.tmp $@

.PHONY: test clean

test:
	echo '$(VERSION)'

clean:
	@rm plugin -fr
