using Common.Authentication.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Common.Authentication.DBHandlers
{
    class UserAccountDbHandler : IDbHandler<IUserAccount>
    {
        #region IDbHandler Interface
        /// <summary>
        /// Returns a single object from the database that has the
        /// given PrimaryKey. It is assumed that the PrimaryKey is
        /// an integer.
        /// </summary>
        /// <param name="pk"></param>
        /// <returns></returns>
        public IUserAccount Get(int pk)
        {
            return null;
        }

        /// <summary>
        /// Returns a single object from the database that matches the
        /// given conditions. The keys in kwars should be a field name
        /// in the class of the model and the values should be the value
        /// for its corresponding field. These will be used as the
        /// conditions for the SELECT statement.
        /// </summary>
        /// <param name="kwargs"></param>
        /// <returns></returns>
        public IUserAccount Get(Dictionary<string, Object> kwargs)
        {
            return null;
        }

        /// <summary>
        /// Returns a list of objects from the database that matches the
        /// given conditions. The keys in kwars should be a field name
        /// in the class of the model and the values should be the value
        /// for its corresponding field. These will be used as the
        /// conditions for the SELECT statement.
        /// </summary>
        /// <param name="kwargs"></param>
        /// <returns></returns>
        public IList<IUserAccount> Filter(Dictionary<string, Object> kwargs)
        {
            return null;
        }

        /// <summary>
        /// Returns every object in the table for this handler.
        /// </summary>
        /// <returns></returns>
        public IList<IUserAccount> All()
        {
            return null;
        }

        /// <summary>
        /// <para>
        /// Returns a list of objects from the database that matches the
        /// given conditions. The keys in kwars should be a field name
        /// in the class of the model and the values should be the value
        /// for its corresponding field. These will be used as the
        /// conditions for the SELECT statement.
        /// </para>
        /// <para>
        /// Each item in the list returned will be updated with the newVals
        /// arguments. This dictionary should have the same format as kwargs.
        /// </para>
        /// </summary>
        /// <param name="kwargs"></param>
        /// <param name="newVals"></param>
        /// <returns></returns>
        public IList<IUserAccount> Update(Dictionary<string, Object> kwargs, Dictionary<string, Object> newVals)
        {
            return null;
        }

        /// <summary>
        /// <para>
        /// Returns a list of objects from the database that matches the
        /// given conditions. The keys in kwars should be a field name
        /// in the class of the model and the values should be the value
        /// for its corresponding field. These will be used as the
        /// conditions for the SELECT statement.
        /// </para>
        /// <para>
        /// Each item in the list returned will be deleted. They no longer
        /// exist in the database after being returned. Their PrimaryKey
        /// field will be cleared as well.
        /// </para>
        /// </summary>
        /// <param name="kwargs"></param>
        /// <returns></returns>
        public IList<IUserAccount> Delete(Dictionary<string, Object> kwargs)
        {
            return null;
        }
        #endregion
    }
}
