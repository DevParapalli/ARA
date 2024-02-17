import { AuthApiError, AuthError } from "@supabase/supabase-js"
import { fail, redirect } from "@sveltejs/kit"

export const actions = {
    update_password: async ({ request, locals }) => {
        const formData = await request.formData()
        const password = formData.get('new_password')

        const { data, error: err } = await locals.supabase.auth.updateUser({
            password
        })

        if (err) {
            if (err instanceof AuthApiError && err.status >= 400 && err.status < 500) {
                return fail(400, {
                    error: "invalidCredentials", invalid: true, message: err.message
                })
            }

            if (err.status && err.status >= 500) {
                return fail(500, {
                    error: "Server error. Please try again later.",
                })
            }

            if (err) {
                return fail(err.status, {
                    error: err.name, message: err.message, invalid: true
                })
            }

            return fail(500, {
                error: 'Server Error' 
            })
            
        }

        redirect(303, "/auth/user_profile");
    },
}

export async function load({locals: { getSession } }) {
    const session = await getSession();
    // if the user is not logged in redirect back to the home page
    if (!session) {
        redirect(303, '/');
    }
  }