import { Link } from "react-router-dom";

const Privacy = () => {
  return (
    <main className="relative min-h-screen overflow-hidden">
      <div className="pointer-events-none fixed inset-0 isolate">
        <div className="absolute inset-0 bg-gradient-overlay" aria-hidden="true" />
        <div className="vintage-grain-layer" aria-hidden="true" />
      </div>

      <div className="relative z-10 mx-auto flex min-h-screen max-w-3xl flex-col px-6 py-16 space-y-6">
        <div className="rounded-3xl bg-white/85 dark:bg-gray-800/75 backdrop-blur-sm border border-border px-8 py-10 shadow-ink">
          <h1 className="text-4xl font-semibold text-black/80 dark:text-white/85">Privacy Notice</h1>
          <p className="mt-3 text-base text-black/70 dark:text-white/75">
            ⚠️ Please avoid sharing personal or sensitive info.
          </p>

          <div className="mt-6 space-y-4 text-base text-black/70 dark:text-white/75 leading-relaxed">
            <section>
              <h2 className="text-xl font-semibold text-black/85 dark:text-white/85">Data controller</h2>
              <p className="mt-1">This site is operated by <strong>Diego Giorgini</strong>.</p>
              <p>
                Contact:{" "}
                <a
                  href="mailto:hello+privacy@diegobit.com"
                  className="text-black/75 underline underline-offset-4 transition hover:text-black dark:text-white/80 dark:hover:text-white"
                >
                  email me
                </a>
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-black/85 dark:text-white/85">What data is processed</h2>
              <ul className="mt-2 list-disc space-y-2 pl-5">
                <li>The <strong>text you type</strong> into the input box.</li>
                <li>
                  <strong>Technical data</strong> needed to run and protect the service, such as IP address,
                  date/time, requested URL and basic browser info (User-Agent).
                </li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-black/85 dark:text-white/85">How your data is used</h2>
              <ul className="mt-2 list-disc space-y-2 pl-5">
                <li>To send your message to <strong>Google Gemini</strong> and return an answer.</li>
                <li>To protect the service from abuse and manage costs (e.g. rate limiting based on IP and request frequency).</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-black/85 dark:text-white/85">Legal basis (GDPR)</h2>
              <ul className="mt-2 list-disc space-y-2 pl-5">
                <li>Providing the AI answers: <strong>performance of a contract / pre-contractual steps</strong> (Art. 6(1)(b) GDPR).</li>
                <li>Security, abuse prevention and cost control: <strong>legitimate interest</strong> (Art. 6(1)(f) GDPR).</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-black/85 dark:text-white/85">Providers</h2>
              <ul className="mt-2 list-disc space-y-2 pl-5">
                <li><strong>Google (Gemini)</strong> processes your messages to generate answers.</li>
                <li><strong>Cloudflare</strong> (Pages, Workers, security features) processes IP and request metadata to deliver and protect the site.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-black/85 dark:text-white/85">Cookies and tracking</h2>
              <ul className="mt-2 list-disc space-y-2 pl-5">
                <li>No <strong>analytics or advertising cookies</strong> and no third-party tracking are used.</li>
                <li>Cloudflare may use <strong>strictly necessary technical cookies</strong> only for security and performance.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-black/85 dark:text-white/85">Logs and retention</h2>
              <ul className="mt-2 list-disc space-y-2 pl-5">
                <li>No custom server-side logging is enabled. Cloudflare may retain minimal technical logs (IP, request metadata, error information) for security and performance according to their default retention.</li>
                <li>I do not build long-term profiles from your usage.</li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-black/85 dark:text-white/85">Your rights</h2>
              <p className="mt-2">
                If you are in the EU/EEA, you can request access, correction, deletion or restriction of your personal
                data, and object to processing based on legitimate interest.
              </p>
              <p>
                To exercise your rights,{" "}
                <a
                  href="mailto:hello+privacy@diegobit.com"
                  className="text-black/75 underline underline-offset-4 transition hover:text-black dark:text-white/80 dark:hover:text-white"
                >
                  send an email
                </a>
                .
              </p>
            </section>
          </div>
        </div>

        <div className="mt-6">
          <Link
            to="/"
            className="text-black/70 underline underline-offset-4 transition hover:text-black dark:text-white/80 dark:hover:text-white"
          >
            Back to home
          </Link>
        </div>
      </div>
    </main>
  );
};

export default Privacy;
