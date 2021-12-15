# Charles Vacine Já

This project was focused on being developed quickly and simply. It has no tests and no great complexity.

With the stage of vaccination against covid 19, the system did not inform when your name was on the vaccination list. This bot was created to act on the vaccination campaign website in Fortaleza CE to search and inform if the name or CPF has been found.

It uses a cron to run a lambda 3x a day and uses the SNS to send an email if someone is found on the list.