ghu Changelog
=============

v1.2.1 - 2017-12-02
-------------------

### Added

- [Ansible][1] script for automatic server configuration.
- Ansible [vault][2] containing (hopefully) any secrets whoever takes on this
  project will need.
- Put Amazon Web Services keys in `[aws]` section in `config.ini`.
- Add login, logout, and registration.
- Add registration confirmation emails.
- Implement email API which sends mail through Amazon Simple Email Service.
- Add organization list page.
- Allow searching organizations.

### Changed

- The `[mail]` section in `config.ini` now holds only the origin email address
  (`source=`), not SMTP connection information. It should always exist.
- Sending email for real and not printing it to the console is now activated by
  the presence of the `[aws]` section, not the `[mail]` section, which must
  always exist.

### Fixed

- The navigation bar now displays on all pages, not just for which the view
  passes the list of navigation bar entries to the template.

### Known issues

- Poor search engine optimization. Searching Google for
  `site:globalhumanitariansunite.org` shows a strange site description, for
  example.
- [Fixtures][3] are missing for setting up navigation bar, so you have to
  create the navigation bar by hand on fresh installations.
- No rate-limiting on registration confirmation emails.
- The rich text editor breaks when adding new toolkit pages. Workaround: add
  the toolkit page, save, and then edit it.
- Ansible script has `globalhumanitariansunite.org` hardcoded as the hostname
  throughout it, making it impossible to test outside production.
- Text is a little small on mobile.
- Site content is editable only in the Django Administration panel. Non-staff
  cannot edit site content.
- Ansible does not fully set up Jenkins.
- nginx needs to be restarted by hand roughly every 90 days to pick up on new
  Let's Encrypt certificate renewed by certbot.
- Virtually non-existent filtering in organization search. Location filtering
  is probably the biggest limitation.
- Jenkins requires about a gigabyte of memory, meaning a more expensive
  server is required to run the site.
- No forum.

[1]: https://github.com/ansible/ansible
[2]: https://docs.ansible.com/ansible/2.4/vault.html
[3]: https://docs.djangoproject.com/en/1.11/howto/initial-data/
