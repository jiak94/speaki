// Given the GitHub branch, tag or pull request,
// compute the tag for the Docker images being build.
//
// Node16 can do most ES2020 and ES2021
const fsp = require("fs").promises;

// Coerce GitHub branch name to Docker image tag requirements
// * alexa/feature/new@@thing==best --> alexa-feature-new--thing--best
const slug = (name) =>
  name
    .replaceAll(/[^a-zA-Z0-9._-]/g, "-")
    .replace(/^[.-]*/, "")
    .substring(0, 128);

(async () => {
  event = JSON.parse(await fsp.readFile(process.env.GITHUB_EVENT_PATH));
  const outputs = { tag: null, target_tag: null };

  if (event.pull_request?.head.repo.fork) {
    outputs.tag = outputs.target_tag = "random-fork";
  } else if ((ref = event.pull_request?.head.ref)) {
    // Pull requests use the name of the branch with the incoming changes
    // * feat/x --> tag: feat-x, target_tag: devel (probably)
    outputs.tag = slug(ref);
    outputs.target_tag = slug(event.pull_request.base.ref);
  } else if (event.ref?.startsWith("refs/heads/")) {
    // Pushes on key branches use the name of the branch
    // Pull request merges into key branches use the name of the target branch
    // * devel --> devel
    // * release/1.0 --> release-1.0
    outputs.tag = outputs.target_tag = slug(event.ref.substring(11));
  } else if (event.ref?.startsWith("refs/tags/")) {
    // Tags on the release branches us the tag name
    // We no longer check if the tag "belongs" to some release branch,
    // because tag belongs to a commit and commit may belong to several branches at once.
    // 1.0.0rc1 --> 1.0.0rc1
    outputs.tag = outputs.target_tag = slug(event.ref.substring(10));
  } else if (event.ref?.startsWith("refs/tags/test-")) {
    // Test tags to validate GHA workflows
    // test-foobar --> test-foobar
    outputs.tag = slug(event.ref.substring(10));
    outputs.target_tag = "dev"; // anything guaranteed to exist
  } else {
    // Unknown event
    outputs.tag = "dev";
    outputs.target_tag = "dev";
  }

  console.log(outputs);
  if (Object.values(outputs).some((v) => !v))
    throw new Error(`Don't know how to tag: ${event}`);

  Object.entries(outputs).map(([k, v]) =>
    console.log(`::set-output name=${k}::${v}`)
  );
})();
