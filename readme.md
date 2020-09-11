# Bellaria Available Flat Script
- will check if any availability on bellaria project zurich
- use sendgrid package

\\ install on Amazon lambda deployment

```shell
pip install --target ./package -r requirements.txt
cd package
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip lambda_function.py utils.py
```