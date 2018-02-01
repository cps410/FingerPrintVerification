using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Common.Models
{
    public class User : IUser
    {
        #region Public Attributes
        /// <summary>
        /// First name of this user.
        /// </summary>
        public String FirstName;

        /// <summary>
        /// Last name of this user.
        /// </summary>
        public String LastName;

        /// <summary>
        /// Middle name of this user.
        /// </summary>
        public String MiddleName;
        #endregion

        #region IUser Interface
        /// <summary>
        /// <para>
        /// Implementation of <see cref="IUser.MatchFingerPrint"/>.
        /// This takes the fingerprint and matches it against the
        /// fingerprint image stored in the database.
        /// </para>
        /// </summary>
        /// <returns>
        /// true if the fingerprint matched that stored in the
        /// database.
        /// </returns>
        public bool MatchFingerPrint()
        {
            return true;
        }
        #endregion
    }
}