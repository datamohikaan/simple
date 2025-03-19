/**
 * Return the portlet server spHelper object.
 *
 * spHelper
 * https://www.ibm.com/support/knowledgecenter/SSHRKX_8.5.0/script/script-portlet/cmd_line_api.html
 *
 * @returns {Object|null} The spHelper object or null if not found
 */
function getSpHelper() {
  // The spHelper object is available in the global namespace, prefixed with a unique id.
  // We only use the first one found.
  for (const key in window) {
    if (window.hasOwnProperty(key) && key.endsWith('spHelper')) {
      return window[key];
    }
  }
  // spHelper object not found.
  return null;
}
 
/**
 * Get the user id.
 *
 * @returns {string | undefined} the user id or undefined if no user session
 */
function getUserId() {
  const spHelper = getSpHelper();
  return spHelper ? spHelper.userId : undefined;
}
 
