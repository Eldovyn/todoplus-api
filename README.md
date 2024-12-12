# TodoPlus API

## Application
1. Website : https://github.com/Eldovyn/todoplus-web

## Technology TodoPlus
1. Flask [Framework Backend Python]
2. MongoDB [Database No-SQL]
3. Redis [Database No-SQL]

<h2>Account Active</h2>
<ul>
    <li>/todoplus/account-active [POST]</li>
    <p>➤ untuk verfikasi email</p>
    <table>
        <tr>
            <th>Headers</th>
            <th>Body</th>
            <th>Type</th>
        </tr>
        <tr>
            <td>Content-Type: application/json</td>
            <td>email</td>
            <td>String</td>
        </tr>
    </table>
</ul>

<h2>Login</h2>
<ul>
    <li>/todoplus/login [POST]</li>
    <p>➤ untuk verfikasi email</p>
    <table>
        <tr>
            <th>Headers</th>
            <th>Body</th>
            <th>Type</th>
        </tr>
        <tr>
            <td>Content-Type: application/json</td>
            <td>email</td>
            <td>String</td>
        </tr>
        <tr>
            <td></td>
            <td>password</td>
            <td>String</td>
        </tr>
    </table>
</ul>


<h2>Me</h2>
<ul>
    <li>/todoplus/@me [GET]</li>
    <p>➤ untuk verfikasi email</p>
    <table>
        <tr>
            <th>Headers</th>
            <th>Query</th>
            <th>Type</th>
        </tr>
        <tr>
            <td>Content-Type: application/json</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Content-Type: application/json</td>
            <td></td>
            <td></td>
        </tr>
    </table>
</ul>

<h2>Register</h2>
<ul>
    <li>/todoplus/register [POST]</li>
    <p>➤ untuk verfikasi email</p>
    <table>
        <tr>
            <th>Headers</th>
            <th>Body</th>
            <th>Type</th>
        </tr>
        <tr>
            <td>Content-Type: application/json</td>
            <td></td>
            <td></td>
        </tr>
    </table>
</ul>

<h2>Reset Password</h2>
<ul>
    <li>/todoplus/register [POST]</li>
    <p>➤ untuk verfikasi email</p>
    <table>
        <tr>
            <th>Headers</th>
            <th>Body</th>
            <th>Type</th>
        </tr>
        <tr>
            <td>Content-Type: application/json</td>
            <td>email</td>
            <td>String</td>
        </tr>
        <tr>
            <td>Authorization: Bearer token</td>
            <td></td>
            <td></td>
        </tr>
    </table>
</ul>