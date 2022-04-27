git log --pretty=format: --name-only --diff-filter=A | sort -u | sed -e 's,.*/,,' | sed '/.java/!d' > tuttifile.txt

git log --pretty=format: --name-only --diff-filter=A | sort -u | sed -e 's,.*/,,' | sed '/.java/!d' | sed '/Test/d' |sed '/test/d' > tuttifile.txt
#toglie file con test nel nome
