README.md: README.Rmd uw_covid_2022.csv
	R -e "knitr::knit('$<')"

uw_covid_2022.csv: scrape_data.py
	./scrape_data.py
	grep '^2' uw_covid_2022.csv > tmp
	cat uw_covid_2022_past.csv tmp > uw_covid_2022.csv
	rm tmp

clean:
	rm uw_covid_2022.csv README.md bar_plots-1.svg
