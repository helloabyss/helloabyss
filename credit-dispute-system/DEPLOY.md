# Going live: step-by-step

This puts the app on the internet at your own web address. Budget about an hour, plus waiting for
accounts to be approved. Rough monthly cost: hosting about $7–$10, domain about $1, email free to $15.

You'll set up four accounts. Do them in this order.

## 1. Domain name (Namecheap, Cloudflare, GoDaddy…)

Buy a domain, e.g. `yourbrand.com`. The app will live at `app.yourbrand.com`.

## 2. Stripe (payments)

1. Sign up at stripe.com and complete business verification. Use your LLC's details.
2. **Products → Add product** "Firm subscription", **recurring monthly** price. Copy its **Price ID**
   (starts `price_`). Consumer one-time payments need no product: the app sets the price itself.
3. **Developers → API keys**: copy the **Secret key** (starts `sk_live_`; use `sk_test_` while testing).
4. Webhooks are set up in step 5, after the site has an address.

## 3. Email sending (Postmark, SendGrid, Amazon SES, or your email provider's SMTP)

The app emails confirmation links, password resets and client signing links. Create an account,
verify your domain (they give you DNS records to add), and copy the **SMTP host, port, username and
password**.

## 4. Render (hosting)

1. Sign up at render.com and connect your GitHub account.
2. **New → Blueprint**, choose this repository, branch `claude/credit-dispute-system`. Render reads
   `render.yaml` and creates the web service with a 1 GB disk for the database.
3. It asks for the settings marked "sync: false". Fill them in:

| Setting | What to enter |
|---|---|
| `DATA_KEY` | The encryption key. Generate it once (below). **Save a copy somewhere safe and offline. If you lose it, every stored case is unreadable. Never change it.** |
| `BASE_URL` | `https://app.yourbrand.com` |
| `COMPANY_NAME` / `COMPANY_ADDRESS` | Your LLC's legal name and business address (they appear on contracts) |
| `STRIPE_SECRET_KEY` | From step 2 |
| `STRIPE_PRO_PRICE_ID` | From step 2 |
| `STRIPE_WEBHOOK_SECRET` | Leave blank for now; fill in at step 5 |
| `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD`, `MAIL_FROM` | From step 3. `MAIL_FROM` like `Your Brand <no-reply@yourbrand.com>` |

To generate `DATA_KEY`, on any computer with Python:
```
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```
(or ask me in a session and I'll generate one).

4. Click **Apply**. The first build takes a few minutes. Visit the `onrender.com` address it shows;
   you should see the home page.

## 5. Connect your domain and Stripe webhooks

1. In Render: your service → **Settings → Custom Domains → Add** `app.yourbrand.com`. Add the DNS
   record it shows at your domain registrar. HTTPS is automatic.
2. In Stripe: **Developers → Webhooks → Add endpoint**
   - URL: `https://app.yourbrand.com/stripe/webhook`
   - Events: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`
   - Copy the **Signing secret** (starts `whsec_`) into Render's `STRIPE_WEBHOOK_SECRET`.
3. In Stripe: **Settings → Billing → Customer portal**: turn it on so firms can manage billing.

## 6. Test everything before telling anyone

With Stripe in **test mode** keys (`sk_test_…`), go through the whole flow on your phone:
create an account, confirm the email, add documents (try the camera), enter accounts, review, sign.
To get past the 3-day cancellation wait while testing, ask me to run the test shortcut, or wait it out.
Pay with Stripe's test card `4242 4242 4242 4242`. Download the letters. Then do the same as a firm at
`/pro`. When it all works, switch to the live keys.

## 7. Backups

Render keeps disk snapshots; check **Disks** in your service for the current schedule and how to restore.
For an off-site copy as well, run `python3 scripts/backup.py /data/cfads.db /data/backups` from the
Render **Shell** tab (or on a schedule) and download the files. Backups are encrypted with `DATA_KEY`, so
store the key separately from them.

## 8. Before the first real customer

- [ ] A lawyer has reviewed the contract, cancellation notice, home-page wording and pricing
      (`webapp/croa.py` lists the exact questions).
- [ ] Registered or bonded in any state that requires it for credit services businesses.
- [ ] Privacy policy and terms of service published, and linked from the site footer.
- [ ] `COMPANY_NAME` and `COMPANY_ADDRESS` are your real legal details.
