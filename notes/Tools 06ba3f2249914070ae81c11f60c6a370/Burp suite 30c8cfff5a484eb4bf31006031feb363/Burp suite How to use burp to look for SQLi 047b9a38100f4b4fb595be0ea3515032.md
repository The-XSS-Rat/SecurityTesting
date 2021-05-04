# Burp suite: How to use burp to look for SQLi

### Introduction

Testing for SQLi using burp suite is not something that's easy but burp suite does allow us several options to make it easier. The biggest problem with searching for SQLi is testing header values we can't normally manipulate without burp suite for example.

### Testing blind SQLi in burp suite

Testing for SQLi might not always be very simple at all. Sometimes it can be as simple as inserting a single quote into every field you see that you suspect interacts with the database. Other times we will not get any feedback if a SQL error occurs so it might seem like the website is not vulnerable to SQLi while in actually it might still be.

In this example we are going to look at how to solve this lab first and then how we could expand on it.

![https://img-a.udemycdn.com/redactor/raw/article_lecture/2021-03-24_00-59-59-e498248d996a199f19d688a795dd00f0.PNG?rOiLypvF-n1yA_SHt1Tal1sJ3orpZ_UVuKdWNhW8Ii1OiuSlvHIt4sYCd9n2Zoj-IYnK9IZiHgDPPXu59a0y23k7OYWx5TKHrV4CPhzZG5qpf5263i7LpMJh0Hi37ZGNox67o6b06EQFNvR6lZXvhZpX8xWE3I4Px2HhgB_yaTyKfS4nkCeqzRDX8uUg-_QgHBUAUg](https://img-a.udemycdn.com/redactor/raw/article_lecture/2021-03-24_00-59-59-e498248d996a199f19d688a795dd00f0.PNG?rOiLypvF-n1yA_SHt1Tal1sJ3orpZ_UVuKdWNhW8Ii1OiuSlvHIt4sYCd9n2Zoj-IYnK9IZiHgDPPXu59a0y23k7OYWx5TKHrV4CPhzZG5qpf5263i7LpMJh0Hi37ZGNox67o6b06EQFNvR6lZXvhZpX8xWE3I4Px2HhgB_yaTyKfS4nkCeqzRDX8uUg-_QgHBUAUg)

### Setting the scope

*Link will be in the downloadeable resource.*

To solve this lab we first have to set our scope correct ofcourse. When starting up the lab, we are given a URL. We can choose to only include this URL in scope or the domain name depending on what we want to do.

If we want to test for just this one lab we can keep the complete URL in scope.

![https://img-a.udemycdn.com/redactor/raw/article_lecture/2021-03-24_01-03-59-3beebfbe1b5cc38ffee7421ac86520fd.PNG?20xacGX25PGSeNRNGUwjXQVtCKSD6E3UF4_XqFJ8_rVwAPf2qgzcmPcCqDBBL7EriXr5IKbHFwjMYp-RZXZcJwNxlMFWKTQ660NE07I65DX5JxEKxxYhvmM_pWnFGo_qE7BRs4fx-s7putNKsrJFUOvXkvXQtj4ACRFZyCbdkoURA4DCRmy9ZzyglxepARKV7rbSpg](https://img-a.udemycdn.com/redactor/raw/article_lecture/2021-03-24_01-03-59-3beebfbe1b5cc38ffee7421ac86520fd.PNG?20xacGX25PGSeNRNGUwjXQVtCKSD6E3UF4_XqFJ8_rVwAPf2qgzcmPcCqDBBL7EriXr5IKbHFwjMYp-RZXZcJwNxlMFWKTQ660NE07I65DX5JxEKxxYhvmM_pWnFGo_qE7BRs4fx-s7putNKsrJFUOvXkvXQtj4ACRFZyCbdkoURA4DCRmy9ZzyglxepARKV7rbSpg)

Or we can select just the domain if we want to test more labs.

![https://img-a.udemycdn.com/redactor/raw/article_lecture/2021-03-24_01-04-22-61acb7b3be205fa28fa6803162cac6f3.PNG?obj8iKws386WTEGikCs2j_hWtAwALkxsgpJI3No_5RXnDaGEIcofAVBfSMCNd1WeRHN8Grf1GWVwb9jwurS7DDTySB5zUUSkrqgJINZuL9CQig5mFwf_vZD0KP6AmFLPRfSBsA6L0FOzPGohrYW_JleOcs0uyNnQ0LCcm-nkb9qmyRXF96lO3JLl19Tah1EQiIvfZg](https://img-a.udemycdn.com/redactor/raw/article_lecture/2021-03-24_01-04-22-61acb7b3be205fa28fa6803162cac6f3.PNG?obj8iKws386WTEGikCs2j_hWtAwALkxsgpJI3No_5RXnDaGEIcofAVBfSMCNd1WeRHN8Grf1GWVwb9jwurS7DDTySB5zUUSkrqgJINZuL9CQig5mFwf_vZD0KP6AmFLPRfSBsA6L0FOzPGohrYW_JleOcs0uyNnQ0LCcm-nkb9qmyRXF96lO3JLl19Tah1EQiIvfZg)

In reality it will heavily depend on the scope of your target what you set here but i will always use the advanced scope control giving me regex capabilities for if need be.

Make sure you also set the out of scope section propperly if need be.

### Solving the lab

To solve this lab we need to visit the homepage and intercept the request. We then need to replace the tracking cookie with the following value:

TrackingId=x'||pg_sleep(10)--

### How to test for this

Since we are talking about blind SQLi we will not be receiving information from the server to even confirm wheter or not we have a SQLi on our hands. In these cases we have several options that allow us to create a noticeable delay (for example a sleep of 10 seconds), however this sleep command will differ from database system to database system.

Oracle`dbms_pipe.receive_message(('a'),10)`

Microsoft`WAITFOR DELAY '0:0:10'`

PostgreSQL`SELECT pg_sleep(10)`

MySQL`SELECT sleep(10)`

We can easily manually test for all of these values

TrackingId=x'||`dbms_pipe.receive_message(('a'),10)`

TrackingId=x'||`WAITFOR DELAY '0:0:10'`

TrackingId=x'||`pg_sleep(10)`

TrackingId=x'||`sleep(10)`

What is happening here is that the server is executing a query in the background. By entering the single quote, we are closing that query, we can then add an OR statement (||). The last step would be to execute our command (see list above).

When the page loads for much longer than the other requests, we know we might have a blind SQLi.

### Other options

We might want to try our SQLi with several other options besides our sleep command and maybe with a combination of single and double quote items. I think you can imagine how this can get confusing fast?

To not have to do this manually for every single request, we can send that request to the intruder.

Right click on the request and click "Send to Intruder". Ones in the intruder select the payload location that you want to test for. In our case we left the x'|| since it will be the same for all requests that we send:

![https://img-a.udemycdn.com/redactor/raw/article_lecture/2021-03-24_01-26-10-d2af3ae4b561fcbd1ab6de6cd1525af9.PNG?AdF-9nSTxNWkUHhjj0hpzHFtOLd6CvzMaUhc9shq0K6RxCHXU5xoYT6-shBeEr60kCLcjG98c9McbFZR5TrzHcz-AefrIF5w1axQBUYPGaml2xc1yNsLefQuHa5FVrIZlmp0QKz1W0r-qNqy8T0I7TPKsobwwxJLjLqo-r9jAc5M1Um5o6cTyXWtrg5wQ54_un3KhA](https://img-a.udemycdn.com/redactor/raw/article_lecture/2021-03-24_01-26-10-d2af3ae4b561fcbd1ab6de6cd1525af9.PNG?AdF-9nSTxNWkUHhjj0hpzHFtOLd6CvzMaUhc9shq0K6RxCHXU5xoYT6-shBeEr60kCLcjG98c9McbFZR5TrzHcz-AefrIF5w1axQBUYPGaml2xc1yNsLefQuHa5FVrIZlmp0QKz1W0r-qNqy8T0I7TPKsobwwxJLjLqo-r9jAc5M1Um5o6cTyXWtrg5wQ54_un3KhA)

We can then fill our payload options with whatever attack vector we wish.

![https://img-a.udemycdn.com/redactor/raw/article_lecture/2021-03-24_01-27-19-35b8111dc8f549e39d202cc0ac8874d9.PNG?BZkTTnGEGlH2qVY48mUiPLslYSMEvekzYT3OucRvDFb599xXt7_zTpPiCDVX316zuXR251KWNGefFhXnZDTNSZi-l1SmSQvWi5mwNvurO6aoXtU-tAhsrNDcImR6U3KCCJgCbnFo3Rkq2MLMda3s4lPxl8cUVU9w0w2Zy1ahX9BvZ4cdfsBfqtu4vzyFSwOhRHAo6g](https://img-a.udemycdn.com/redactor/raw/article_lecture/2021-03-24_01-27-19-35b8111dc8f549e39d202cc0ac8874d9.PNG?BZkTTnGEGlH2qVY48mUiPLslYSMEvekzYT3OucRvDFb599xXt7_zTpPiCDVX316zuXR251KWNGefFhXnZDTNSZi-l1SmSQvWi5mwNvurO6aoXtU-tAhsrNDcImR6U3KCCJgCbnFo3Rkq2MLMda3s4lPxl8cUVU9w0w2Zy1ahX9BvZ4cdfsBfqtu4vzyFSwOhRHAo6g)

We will then have to study every request to see if we can find requests that are different from the rest in any way.

![https://img-a.udemycdn.com/redactor/raw/article_lecture/2021-03-24_01-28-37-dfa611f89d446df2133c933af2e2074c.PNG?wpUjdspFkIa5F4KESGv2wKOWAsrF00NRlOUC7rr6v4wRk5CNa55L37RzdPQtr3xY5wZ9N7uvKkwwj4YnsH5evc0KaB54JvSQvzjheFurUeJJfPX6P-fJvG824vF63XUQ75Uq8mVnQkHlsGJhLPt8fLI3P_zaxWyU_fWnZhYFMe_lP_kBQp9zDL6HACphfm3o0GrxTA](https://img-a.udemycdn.com/redactor/raw/article_lecture/2021-03-24_01-28-37-dfa611f89d446df2133c933af2e2074c.PNG?wpUjdspFkIa5F4KESGv2wKOWAsrF00NRlOUC7rr6v4wRk5CNa55L37RzdPQtr3xY5wZ9N7uvKkwwj4YnsH5evc0KaB54JvSQvzjheFurUeJJfPX6P-fJvG824vF63XUQ75Uq8mVnQkHlsGJhLPt8fLI3P_zaxWyU_fWnZhYFMe_lP_kBQp9zDL6HACphfm3o0GrxTA)