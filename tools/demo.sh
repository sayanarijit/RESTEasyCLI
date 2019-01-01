recli init

cat sites.yml
cat auth.yml
cat headers.yml
cat saved.yml

clear

recli list-endpoints

recli get testing/todos

recli list testing/todos --kwargs userId=1 --fit-width

recli show testing/todos/1 --fit-width

recli delete testing/todo1

clear

recli list-saved

recli do remind_shopping

recli redo remind_shopping --update_kwargs userId=1 "title=watch naruto" --fake

recli redo remind_shopping --update_kwargs userId=1 "title=watch naruto" --fake --save_as my_request


recli show-saved my_request

cat saved.yml

recli do my_request
