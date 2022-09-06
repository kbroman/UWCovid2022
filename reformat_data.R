# Read uw_covid_2022.csv
# Add overall values
# reorganize columns

file <- "uw_covid_2022.csv"
oldfile <- "uw_covid_2022_past.csv"

# read data
x <- read.csv(file)

# add columns with overall values
x$Total_overall <- x$Total_employees + x$Total_students
x$Positive_overall <- x$Positive_employees + x$Positive_students

# take column order from the other file
y <- read.csv(oldfile)
x <- x[,colnames(y)]

# write data
write.table(x, file=file, sep=",", quote=FALSE, col.names=TRUE, row.names=FALSE)
