VERSION=0.3\(b2\)
LASTCHANGE=05\/07\/2013\ 17:57
BUILDTIME=$(shell date '+%m\/%d\/%Y\ %H:%M')


release: plugin/autocommand.vim
debug: plugin/autocommand.vim plugin/autocommand.py

#old split case
#sed -n '1,40p' src/autocommand.vim > $@.tmp
#sed -n '42,126p' src/autocommand.vim >> $@.tmp

plugin/autocommand.vim: src/autocommand.vim src/autocommand.py
	@test -d plugin || mkdir plugin
	awk -v RS='#\\$$file:autocommand.py\\$$' '{print $$0 > "$@.tmp_"NR}' src/autocommand.vim
	sed -i '$$d' $@.tmp_1
	sed -i '1d;$$d' $@.tmp_2
	mv -f $@.tmp_1 $@.tmp
	cat src/autocommand.py >> $@.tmp
	cat $@.tmp_2 >> $@.tmp && rm $@.tmp_2 -f
	sed -i 's/$$version\$$/$(VERSION)/g' $@.tmp
	sed -i 's/$$lastChange\$$/$(LASTCHANGE)/g' $@.tmp
	sed -i 's/$$buildTime\$$/$(BUILDTIME)/g' $@.tmp
	mv $@.tmp $@

plugin/autocommand.py: src/autocommand.py
	@test -d plugin || mkdir plugin
	cp $< $@.tmp
	sed -i 's/$$version\$$/$(VERSION)/g' $@.tmp
	sed -i 's/$$lastChange\$$/$(LASTCHANGE)/g' $@.tmp
	sed -i 's/$$buildTime\$$/$(BUILDTIME)/g' $@.tmp
	mv $@.tmp $@

test:
	awk -v RS='#\\$$file:autocommand.py\\$$' '{print $$0 > "abc.tmp_"NR}' src/autocommand.vim

clean:
	@rm plugin -fr

.PHONY: test clean
