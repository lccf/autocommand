VERSION=0.3\(beta\)
LASTCHANGE=04\/13\/2013\ 14:34
BUILDTIME=$(shell date '+%m\/%d\/%Y\ %H:%M')


release: plugin/autocommand.vim
debug: plugin/autocommand.debug.vim plugin/autocommand.debug.py

all: release debug

plugin/autocommand.vim: src/autocommand.vim src/autocommand.py
	@cd plugin || mkdir plugin
	sed -n '1,40p' src/autocommand.vim > $@.tmp
	cat src/autocommand.py >> $@.tmp
	sed -n '42,126p' src/autocommand.vim >> $@.tmp
	sed -i 's/$$version\$$/$(VERSION)/g' $@.tmp
	sed -i 's/$$lastChange\$$/$(LASTCHANGE)/g' $@.tmp
	sed -i 's/$$buildTime\$$/$(BUILDTIME)/g' $@.tmp
	mv $@.tmp $@

plugin/autocommand.debug.vim: src/autocommand.vim
	@cd plugin || mkdir plugin
	cp $< $@.tmp
	sed -i 's/$$version\$$/$(VERSION)/g' $@.tmp
	sed -i 's/$$lastChange\$$/$(LASTCHANGE)/g' $@.tmp
	sed -i 's/$$buildTime\$$/$(BUILDTIME)/g' $@.tmp
	mv $@.tmp $@
plugin/autocommand.debug.py: src/autocommand.py
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
