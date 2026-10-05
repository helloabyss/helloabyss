// Progressive web app + native (Capacitor) glue. No personal data is stored on the device.
(function () {
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js").catch(function () {});
  }

  // Android/desktop "Install app" button (iPhone uses Share > Add to Home Screen; see /install).
  var deferred = null;
  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault();
    deferred = e;
    var b = document.getElementById("install-btn");
    if (b) b.hidden = false;
  });
  document.addEventListener("click", function (e) {
    var t = e.target.closest ? e.target.closest("#install-btn, a[data-external]") : null;
    if (!t) return;
    if (t.id === "install-btn" && deferred) {
      e.preventDefault();
      deferred.prompt();
      deferred = null;
      t.hidden = true;
    }
    var cap = window.Capacitor;
    if (t.hasAttribute("data-external") && cap && cap.isNativePlatform && cap.isNativePlatform() && cap.Plugins.Browser) {
      e.preventDefault();
      cap.Plugins.Browser.open({ url: t.href });  // system browser, outside the app
    }
  });

  // In the store apps: schedule on-device reminders for dispute deadlines.
  var cap = window.Capacitor;
  if (cap && cap.isNativePlatform && cap.isNativePlatform() && cap.Plugins.LocalNotifications && document.body.dataset.loggedIn === "1") {
    var LN = cap.Plugins.LocalNotifications;
    LN.requestPermissions().then(function (perm) {
      if (perm.display !== "granted") return;
      return fetch("/api/reminders", { credentials: "same-origin" })
        .then(function (r) { return r.ok ? r.json() : { reminders: [] }; })
        .then(function (data) {
          return LN.getPending().then(function (p) {
            var old = (p.notifications || []).map(function (n) { return { id: n.id }; });
            return (old.length ? LN.cancel({ notifications: old }) : Promise.resolve()).then(function () {
              var list = data.reminders.map(function (r) {
                return { id: r.id, title: r.title, body: r.body, schedule: { at: new Date(r.at) } };
              });
              if (list.length) return LN.schedule({ notifications: list });
            });
          });
        });
    }).catch(function () {});
  }
})();
