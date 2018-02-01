using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Common.Models
{
    public class UserAccount : IUserAccount
    {
        #region Public Attributes
        /// <summary>
        /// The User object that owns this account.
        /// </summary>
        public IUser User;

        public string Username;
        #endregion

        #region IUserAccount Interface
        /// <summary>
        /// <para>
        /// Implementation of <see cref="IUserAccount.Authenticate(string)"/>.
        /// Authenticates this account by testing the passed in
        /// password guess against the password stored in the database.
        /// </para>
        /// <para>
        /// The password stored in the database is encrypted.
        /// To match these two, the same encryption technique used
        /// to encrypt the true password will be used on the password
        /// passed in here. If the two encryptions are the same,
        /// true is returned.
        /// </para>
        /// <para>
        /// The password parameter should not be encrypted when passed
        /// in. It should be passed in just as the user entered it.
        /// </para>
        /// </summary>
        /// <param name="password">The guess at the password for this account</param>
        /// <returns>
        /// True if the password matches that stored in the database.
        /// False otherwise.
        /// </returns>
        public bool Authenticate(string password)
        {
            return true;
        }
        #endregion
    }
}