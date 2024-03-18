<script>
    export let data
</script>

<h2>User profile</h2>
{data.session.user.email}
{JSON.stringify(data.notebooks)}
{JSON.stringify(data.cells)}
<!-- <p><a href="/auth/update_email">Change your email</a></p> -->
<p><a href="/auth/update_password">Change password</a></p>
<!-- <p><a href="/auth/delete_user">Delete my account</a></p> -->