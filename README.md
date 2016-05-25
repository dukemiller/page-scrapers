## Page Parsers 

Some simple page parsers for retrieving random things from pages that don't
have an api.


#### Notes

Most of the times the scripts are written in that they only work for a single case and
aren't generic, e.g. only downloading the content of a single users page on flickr without
any user prompting, but changing them to work for other pages generally isn't hard 
and/or is an eventual goal.

Sometimes the scripts are meant to be just a quick procedural run and their logic
isn't modularized, but if it gets past some arbitrary amount of LoC (~40?) then
I tend to split it up.