# Tutorial at https://makefiletutorial.com/
# Docs at https://www.gnu.org/software/make/manual/make.html

src_dir := src


.PHONY:
format:
	python -m black $(src_dir)

.PHONY:
test:
	python -m unittest --failfast

# TODO
.PHONY:
coverage:
	coverage run -m unittest; coverage report -m

.PHONY:
run:
	flask --app $(src_dir)/app --debug run
